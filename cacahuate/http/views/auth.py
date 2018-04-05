from datetime import datetime
from flask import request, jsonify, abort
from cacahuate.errors import AuthenticationError
from cacahuate.http.errors import Unauthorized
from cacahuate.http.wsgi import app
from cacahuate.models import User, Token
from random import choice
from string import ascii_letters


@app.route('/v1/auth/signin/<AuthProvider:backend>', methods=['POST'])
def signin(backend):
    try:
        backend_user = backend.authenticate(**request.form.to_dict())
    except AuthenticationError:
        abort(401, 'Provided user credentials are invalid')

    user = backend_user.get_user()

    # creates auth token
    if user.proxy.tokens.count() > 0:
        token = user.proxy.tokens.get()[0]
    else:
        token = ''.join(choice(ascii_letters) for _ in range(32))
        token = Token(token=token).save()
        token.proxy.user.set(user)

    return jsonify({
        'data': {
            'username': user.identifier,
            'token': token.token,
        }
    })


@app.route('/v1/auth/whoami')
def whoami():
    identifier = request.authorization['username']
    token = request.authorization['password']

    user = User.get_by('identifier', identifier)
    token = Token.get_by('token', token)

    if user is None or \
       token is None or \
       token.proxy.user.get().id != user.id:
        raise Unauthorized([{
            'detail': 'Your credentials are invalid, sorry',
            'where': 'request.authorization',
        }])

    return jsonify({
        'data': user.to_json(),
    })
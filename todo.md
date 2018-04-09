# Colores

## primera iteración

* iniciar un proceso guarda formularios en campo status
* continuar un proceso guarda formularios en campo status
* volver al pasado restaura los formularios del nodo al que cayó con las fechas más recientes
    - probar con varios registros
* regresar dispara búsqueda de padres de punteros para saber quienes sobreviven y quienes no
* api de status de un nodo (último registro de estado de ese nodo)

# Multiauth

* cada respuesta de usuario elimina la relación entre el usuario y el puntero
* validar que un usuario sin relación con el puntero no pueda responder
* handler no elimina ni avanza puntero hasta que esté satisfecho el número de respondientes
* último en responder elimina puntero y encola petición
* notificar usuarios no crea punteros a menos que haya un formulario
* terminar un nodo elimina todas las relaciones entre puntero y usuario (que podrían ser muchas)

# Otros

* handler debe poder cargar hierarchy externos
* mecanismo de suspensión de procesos en caso de falla crítica para no matar otros procesos

# comunicación externa

* forma de hacer peticiones desde un nodo
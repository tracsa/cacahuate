import xml.etree.ElementTree as ET

def etree_from_list(root:ET.Element, nodes:[ET.Element]) -> ET.ElementTree:
    ''' Returns a built ElementTree from the list of its members '''
    root = ET.Element(root.tag, attrib=root.attrib)
    root.extend(nodes)

    return ET.ElementTree(root)

def nodes_from(node:ET.Element, graph):
    ''' returns an iterator over the (node, edge)s that can be reached from
    node '''
    for edge in graph.findall(".//*[@from='{}']".format(node.attrib['id'])):
        yield (graph.find(".//*[@id='{}']".format(edge.attrib['to'])), edge)

def has_no_incoming(node:ET.Element, graph:'root ET.Element'):
    ''' returns true if this node has no edges pointing to it '''
    return len(graph.findall(".//*[@to='{}']".format(node.attrib['id']))) == 0

def has_edges(graph:'root ET.Element'):
    ''' returns true if the graph still has edge elements '''
    return len(graph.findall("./connector")) > 0

def topological_sort(start_node:ET.Element, graph:'root ET.Element') -> ET.ElementTree:
    ''' sorts topologically the given xml element tree, source:
    https://en.wikipedia.org/wiki/Topological_sorting '''
    sorted_elements = [] # sorted_elements ← Empty list that will contain the sorted elements
    no_incoming = [(start_node, None)] # (node, edge that points to this node)

    while len(no_incoming) > 0:
        node, edge = no_incoming.pop()

        if edge is not None:
            sorted_elements.append(edge)
        sorted_elements.append(node)

        for m, edge in nodes_from(node, graph=graph):
            graph.remove(edge)

            if has_no_incoming(m, graph):
                no_incoming.append((m, edge))

    if has_edges(graph) > 0:
        raise Exception('graph is cyclic')

    return etree_from_list(graph, sorted_elements)
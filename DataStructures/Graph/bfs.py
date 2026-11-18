"""
Recorrido en anchura (BFS) sobre un grafo dirigido.

La estructura de busqueda es un mapa cuya llave es la llave del vertice
alcanzado y cuyo valor es un diccionario con:

- ``marked``: True si el vertice fue visitado.
- ``edge_from``: llave del vertice desde el que se llego. Para el origen es None.
- ``dist_to``: numero de arcos desde el origen hasta el vertice.
"""

from DataStructures.Graph import digraph as G
from DataStructures.List import array_list as lt
from DataStructures.Map import map_linear_probing as mp
from DataStructures.Queue import queue as q
from DataStructures.Stack import stack as st


def bfs(my_graph, source):
    """
    Funcion mascara: inicia el recorrido BFS desde ``source``.

    :returns: Mapa con los vertices alcanzables desde ``source``
    """
    visited_map = mp.new_map(G.order(my_graph), 0.5)
    mp.put(visited_map, source, {"marked": True, "edge_from": None, "dist_to": 0})
    bfs_vertex(my_graph, source, visited_map)
    return visited_map


def bfs_vertex(my_graph, source, visited_map):
    """
    Recorre el grafo por niveles desde ``source`` usando una cola.
    Cada vertice se marca la primera vez que se descubre, asi queda
    guardado el camino con menos arcos desde el origen.

    :returns: El mapa de visitados actualizado
    """
    cola = q.new_queue()
    q.enqueue(cola, source)
    while not q.is_empty(cola):
        vertex = q.dequeue(cola)
        dist_vertex = mp.get(visited_map, vertex)["dist_to"]
        adjacent_keys = G.adjacents(my_graph, vertex)
        for i in range(lt.size(adjacent_keys)):
            w = lt.get_element(adjacent_keys, i)
            if not mp.contains(visited_map, w):
                mp.put(visited_map, w, {"marked": True,
                                        "edge_from": vertex,
                                        "dist_to": dist_vertex + 1})
                q.enqueue(cola, w)
    return visited_map


def has_path_to(key_v, visited_map):
    """
    Indica si hay camino desde el origen hasta ``key_v``.
    Precondicion: se ejecuto ``bfs``.
    """
    info = mp.get(visited_map, key_v)
    return info is not None and info["marked"]


def path_to(key_v, visited_map):
    """
    Retorna una pila con el camino desde el origen hasta ``key_v``
    (el origen queda en el tope). Si no hay camino retorna None.
    Precondicion: se ejecuto ``bfs``.
    """
    if not has_path_to(key_v, visited_map):
        return None
    path = st.new_stack()
    current = key_v
    while current is not None:
        st.push(path, current)
        current = mp.get(visited_map, current)["edge_from"]
    return path

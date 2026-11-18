"""
Algoritmo de Dijkstra sobre un grafo dirigido con pesos no negativos.

Se usa la estructura de ``dijsktra_structure``:

- ``source``: llave del vertice origen.
- ``visited``: mapa cuya llave es la llave del vertice y cuyo valor es un
  diccionario con:
    - ``marked``: True cuando ya se fijo su distancia minima.
    - ``edge_from``: llave del vertice desde el que se llego. Para el origen es None.
    - ``dist_to``: distancia minima conocida desde el origen.
- ``pq``: cola de prioridad (min) con parejas (distancia, vertice).

Version "lazy": cuando se mejora la distancia de un vertice se vuelve a
insertar en la cola. Las entradas viejas se ignoran porque el vertice ya
queda marcado.
"""

import math

from DataStructures.Graph import digraph as G
from DataStructures.Graph import edge as E
from DataStructures.Graph import dijsktra_structure as ds
from DataStructures.List import array_list as lt
from DataStructures.Map import map_linear_probing as mp
from DataStructures.Priority_queue import priority_queue as pq
from DataStructures.Stack import stack as st


def dijkstra(my_graph, source):
    """
    Calcula los caminos de costo minimo desde ``source`` a todos los
    vertices alcanzables del grafo.

    :returns: Estructura de busqueda de dijkstra
    """
    aux_structure = ds.new_dijsktra_structure(source, G.order(my_graph))
    visited = aux_structure["visited"]
    cola = aux_structure["pq"]

    mp.put(visited, source, {"marked": False, "edge_from": None, "dist_to": 0})
    pq.insert(cola, 0, source)

    while not pq.is_empty(cola):
        vertex = pq.remove(cola)
        info_vertex = mp.get(visited, vertex)
        # Entrada vieja de la cola: el vertice ya tiene su distancia final
        if info_vertex["marked"]:
            continue
        info_vertex["marked"] = True

        edges = G.edges_vertex(my_graph, vertex)
        for i in range(lt.size(edges)):
            edge = lt.get_element(edges, i)
            relax(visited, cola, vertex, info_vertex["dist_to"], edge)

    return aux_structure


def relax(visited, cola, vertex, dist_vertex, edge):
    """
    Relaja el arco ``vertex -> w``: si pasando por ``vertex`` se llega
    a ``w`` con menor distancia, se actualiza y se mete a la cola.
    """
    w = E.to(edge)
    nueva_dist = dist_vertex + E.weight(edge)
    info_w = mp.get(visited, w)
    if info_w is None:
        mp.put(visited, w, {"marked": False, "edge_from": vertex, "dist_to": nueva_dist})
        pq.insert(cola, nueva_dist, w)
    elif not info_w["marked"] and nueva_dist < info_w["dist_to"]:
        info_w["dist_to"] = nueva_dist
        info_w["edge_from"] = vertex
        pq.insert(cola, nueva_dist, w)


def dist_to(key_v, aux_structure):
    """
    Retorna la distancia minima desde el origen hasta ``key_v``.
    Si no hay camino retorna infinito.
    Precondicion: se ejecuto ``dijkstra``.
    """
    info = mp.get(aux_structure["visited"], key_v)
    if info is None:
        return math.inf
    return info["dist_to"]


def has_path_to(key_v, aux_structure):
    """
    Indica si hay camino desde el origen hasta ``key_v``.
    Precondicion: se ejecuto ``dijkstra``.
    """
    info = mp.get(aux_structure["visited"], key_v)
    return info is not None and info["marked"]


def path_to(key_v, aux_structure):
    """
    Retorna una pila con el camino de costo minimo desde el origen hasta
    ``key_v`` (el origen queda en el tope). Si no hay camino retorna None.
    Precondicion: se ejecuto ``dijkstra``.
    """
    if not has_path_to(key_v, aux_structure):
        return None
    path = st.new_stack()
    current = key_v
    while current is not None:
        st.push(path, current)
        current = mp.get(aux_structure["visited"], current)["edge_from"]
    return path

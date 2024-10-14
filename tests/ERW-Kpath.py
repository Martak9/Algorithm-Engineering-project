import random

from networkit import graphtools
from networkit.graph import Graph


def assign_normalized_degree(G: Graph):
    degrees = {}
    total_nodes = G.numberOfNodes()
    for node in G.iterNodes():
        degree = G.degree(node)
        normalized_degree = degree / total_nodes
        degrees[node] = normalized_degree
    return degrees


def assign_uniform_weights(G: Graph):
    total_edges = G.numberOfEdges()
    for u, v in G.iterEdges():
        G.setWeight(u, v, 1.0 / total_edges)


def ERW_KPath(G: Graph, k, p, b):
    assign_normalized_degree(G)
    assign_uniform_weights(G)
    for _ in range(p):
        N = 0
        vn = graphtools.randomNode(G)
        messagePropagation(vn, N, k, b, G)

"""
# Se gli archi sono già stati tutti visitati?
def random_edge(G: Graph, n, Tn):
    edge_from_node = []
    for edge in G.iterEdges():
        if edge[0] == n:
            edge_from_node.append(edge)
    em = random.choice(edge_from_node)
    while Tn.get('em', 0) != 0:
        em = random.choice(edge_from_node)
    return em
"""

def random_edge(G: Graph, n, Tn):
    edge_from_node = []
    for edge in G.iterEdges():
        if edge[0] == n and edge not in Tn:
            edge_from_node.append(edge)
    if not edge_from_node:
        return None  # Non ci sono archi disponibili
    return random.choice(edge_from_node)

"""
# Se non ci sono nodi vicini?
def neighbor_node(G: Graph, n, em):
    for neighbor in G.iterNeighbors(n):
        if em.hasEdge(n, neighbor) or em.hasEdge(neighbor, n):
            return neighbor
    return None
"""

def neighbor_node(G: Graph, n, em):
    u, v = em  # Spacchetta la tupla dell'arco
    if u == n:
        return v
    elif v == n:
        return u
    else:
        return None  # L'arco non è connesso al nodo n


def messagePropagation(n, N, k, b, G: Graph):
    Tn = {}
    while N < k and G.degree(n) > sum(Tn.values()):
        em = random_edge(G, n, Tn)
        if em is None:
            break
        vn = neighbor_node(G, n, em)
        if vn is None:
            continue
        Tn[em] = 1
        G.setWeight(n, vn, G.weight(n, vn) + b)
        n = vn
        N += 1

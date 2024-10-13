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
def random_edge(G: Graph, Tn):
    em = graphtools.randomEdge(G)
    while Tn.get('em', 0) != 0:
        em = graphtools.randomEdge(G)
    return em
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

# Se non ci sono nodi vicini?
def neighbor_node(G: Graph, n, em):
    for neighbor in G.iterNeighbors(n):
        if em.hasEdge(n, neighbor) or em.hasEdge(neighbor, n):
            return neighbor
    return None


def messagePropagation(n, N, k, b, G: Graph):
    Tn = {}
    while N < k and G.degree(n) > sum(Tn.values()):
        em = random_edge(G, Tn)
        vn = neighbor_node(G, n, em)
        Tn[em] = 1
        G.setWeight(n, vn, G.weight(n, vn) + b)
        n = vn
        N += 1

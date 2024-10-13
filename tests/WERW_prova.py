import random
from networkit import Graph


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
    weight = 1.0 / total_edges
    for u, v in G.iterEdges():
        G.setWeight(u, v, weight)


def WERW_KPath(G: Graph, j, q, b):
    normalized_degrees = assign_normalized_degree(G)
    assign_uniform_weights(G)

    for _ in range(q):
        vn = random.choices(list(G.iterNodes()), weights=list(normalized_degrees.values()), k=1)[
            0]  # Selezione pesata del nodo iniziale
        N = 0
        messagePropagation(vn, N, j, b, G)

    # Assegna i pesi finali come indici di centralità
    # Non è necessario fare nulla qui, i pesi sono già aggiornati


def messagePropagation(vn, N, j, b, G: Graph):
    traversed_edges = set()

    while N < j and G.degree(vn) > len(
            [e for e in G.iterNeighbors(vn) if (vn, e) in traversed_edges or (e, vn) in traversed_edges]):
        available_edges = [(vn, e) for e in G.iterNeighbors(vn) if
                           (vn, e) not in traversed_edges and (e, vn) not in traversed_edges]

        if not available_edges:
            break

        edge_weights = [G.weight(e[0], e[1]) for e in available_edges]
        em = available_edges[
            random.choices(range(len(available_edges)), weights=edge_weights, k=1)[0]]  # Selezione pesata dell'arco
        vn_next = em[1]

        # Aggiorna il peso dell'arco
        current_weight = G.weight(em[0], em[1])
        G.setWeight(em[0], em[1], current_weight + b)

        traversed_edges.add(em)
        vn = vn_next
        N += 1


# Esempio di utilizzo
def main():
    # Crea un grafo di esempio (pesato)
    G = Graph(5, weighted=True, directed=False)
    G.addEdge(0, 1, 1.0)
    G.addEdge(1, 2, 1.0)
    G.addEdge(2, 3, 1.0)
    G.addEdge(3, 4, 1.0)
    G.addEdge(4, 0, 1.0)

    # Parametri dell'algoritmo
    j = 3  # Lunghezza massima del percorso
    q = G.numberOfEdges() - 1  # Numero di iterazioni
    b = 1.0 / G.numberOfEdges()  # Bonus

    WERW_KPath(G, j, q, b)

    # Stampa i risultati
    print("Edge Centrality Values:")
    for u, v in G.iterEdges():
        print(f"Edge ({u}, {v}): {G.weight(u, v)}")


if __name__ == "__main__":
    main()
import random
import time

import networkit as nk
from networkit import Graph
from csv_writer import CsvWriter


def assign_normalized_degree(G: Graph):
    degrees = {}
    total_edges = G.numberOfEdges()
    for node in G.iterNodes():
        degree = G.degree(node)
        normalized_degree = degree / total_edges
        degrees[node] = normalized_degree
    return degrees


def initialize_weights(G: Graph):
    omega = {}
    uniform_weight = 1.0 / G.numberOfEdges()
    for u, v in G.iterEdges():
        if u < v:
            omega[(u, v)] = uniform_weight
        else:
            omega[(v, u)] = uniform_weight
    return omega


def ERW_KPath(G: Graph, kappa: int, rho: int, beta: float):
    normalized_degrees = assign_normalized_degree(G)
    omega = initialize_weights(G)

    for i in range(rho):
        vn = random.choice(list(G.iterNodes()))
        print(f"\nIterazione {i + 1}:")
        print(f"Nodo di partenza scelto: {vn}")
        MessagePropagation(G, vn, kappa, omega, beta)
        print("Current edge weights:")
        for edge, weight in omega.items():
            print(f"Edge {edge}: {weight}")

    return omega


def MessagePropagation(G: Graph, start: int, kappa: int, omega: dict, beta: float):
    path = [start]
    print(f"Cammino: {start}", end="")

    for _ in range(kappa - 1):  # kappa - 1 perché il nodo di partenza è già nel cammino
        unvisited_neighbors = [v for v in G.iterNeighbors(path[-1]) if v not in path]

        if not unvisited_neighbors:
            print(" (terminato: nessun vicino non visitato)")
            break

        next_node = random.choice(unvisited_neighbors)
        print(f" -> {next_node}", end="")

        update_edge_weight(omega, path[-1], next_node, beta)
        path.append(next_node)

    print()


def update_edge_weight(omega: dict, u: int, v: int, beta: float):
    key = (min(u, v), max(u, v))
    omega[key] = omega.get(key, 0) + beta


def mark_edge_visited(omega: dict, u: int, v: int):
    key = (min(u, v), max(u, v))
    omega[key] = 1


def erw_centrality_algorithm(G: Graph):
    kappa = 5  # Maximum path length
    rho = G.numberOfEdges()  # Number of iterations
    beta = 1.0 / G.numberOfEdges()  # Weight increment

    omega = ERW_KPath(G, kappa, rho, beta)

    edge_centrality = [(u, v, weight) for (u, v), weight in omega.items()]
    edge_centrality_sorted = sorted(edge_centrality, key=lambda x: x[2], reverse=True)

    return edge_centrality_sorted


def main():
    start_time = time.time()
    # Load graph
    reader = nk.graphio.EdgeListReader(separator=" ", firstNode=0, continuous=False, directed=False)
    G = reader.read("./graph/graph(n=10, m=30).txt")

    print(f"Grafo caricato. Nodi: {G.numberOfNodes()}, Archi: {G.numberOfEdges()}")

    edge_centrality_sorted = erw_centrality_algorithm(G)

    print("\nFinal Edge Centrality Values (sorted):")
    csv_data = []
    for u, v, weight in edge_centrality_sorted:
        dict_csv_row = {"edge": f"{u}, {v}", "centrality": weight}
        csv_data.append(dict_csv_row)
        print(f"Edge ({u}, {v}): {weight}")
    CsvWriter().write(csv_data, "./csv_files/centrality_ERW", ["edge", "centrality"])
    end_time = time.time()
    print(f"Total script execution time: {end_time - start_time:.2f} seconds")


if __name__ == "__main__":
    main()
import random
import networkit as nk
from networkit import Graph
from csv_writer import CsvWriter
import time



def assign_normalized_degree(G: Graph):
    start_time = time.time()
    total_edges = G.numberOfEdges()
    result = {node: G.degree(node) / total_edges for node in G.iterNodes()}
    end_time = time.time()
    print(f"assign_normalized_degree execution time: {end_time - start_time:.2f} seconds")
    return result


def initialize_weights(G: Graph):
    start_time = time.time()
    uniform_weight = 1.0 / G.numberOfEdges()
    result = {(min(u, v), max(u, v)): uniform_weight for u, v in G.iterEdges()}
    end_time = time.time()
    print(f"initialize_weights execution time: {end_time - start_time:.2f} seconds")
    return result


def WERW_KPath(G: Graph, kappa: int, rho: int, beta: float):
    normalized_degrees = assign_normalized_degree(G)
    omega = initialize_weights(G)

    for i in range(rho):
        vn = random.choices(list(G.iterNodes()), weights=list(normalized_degrees.values()), k=1)[0]
        print(f"\nIterazione {i + 1}:")
        print(f"Nodo di partenza scelto: {vn}")
        MessagePropagation(G, vn, kappa, omega, beta)
        print("Current edge weights:")
        for edge, weight in omega.items():
            print(f"Edge {edge}: {weight}")

    return omega


def MessagePropagation(G: Graph, start: int, kappa: int, omega: dict, beta: float):
    path = [start]
    visited = set([start])
    print(f"Cammino: {start}", end="")

    for _ in range(kappa - 1):
        current = path[-1]
        neighbors = list(G.iterNeighbors(current))
        unvisited_neighbors = [v for v in neighbors if v not in visited]

        if not unvisited_neighbors:
            print(" (terminato: nessun vicino non visitato)")
            break

        total_weight = sum(omega.get((min(current, v), max(current, v)), 0) for v in unvisited_neighbors)
        probs = [omega.get((min(current, v), max(current, v)), 0) / total_weight for v in unvisited_neighbors]

        next_node = random.choices(unvisited_neighbors, weights=probs, k=1)[0]
        print(f" -> {next_node}", end="")

        edge = (min(current, next_node), max(current, next_node))
        omega[edge] += beta

        path.append(next_node)
        visited.add(next_node)

    print()  # Stampa una nuova riga alla fine del percorso


def werw_centrality_algorithm(G: Graph):
    start_time = time.time()
    kappa = 5  # Lunghezza massima del cammino
    rho = G.numberOfEdges()  # Numero di iterazioni
    beta = 1.0 / G.numberOfEdges()

    omega = WERW_KPath(G, kappa, rho, beta)

    result = sorted(((u, v, weight) for (u, v), weight in omega.items()), key=lambda x: x[2], reverse=True)
    end_time = time.time()
    print(f"werw_centrality_algorithm total execution time: {end_time - start_time:.2f} seconds")
    return result


def main():
    start_time = time.time()
    reader = nk.graphio.EdgeListReader(separator=" ", firstNode=0, continuous=False, directed=False)
    G = reader.read("./graph/graph(n=10, m=30).txt")
    print(f"Graph loaded. Nodes: {G.numberOfNodes()}, Edges: {G.numberOfEdges()}")

    edge_centrality_sorted = werw_centrality_algorithm(G)

    csv_data = [{"edge": f"{u}, {v}", "centrality": weight} for u, v, weight in edge_centrality_sorted]
    CsvWriter().write(csv_data, "./csv_files/centrality_ERW", ["edge", "centrality"])

    end_time = time.time()
    print(f"Total script execution time: {end_time - start_time:.2f} seconds")


if __name__ == "__main__":
    main()
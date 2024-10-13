import random
import time
import networkit as nk
from networkit import Graph
from csv_writer import CsvWriter

def assign_normalized_degree(G: Graph):
    start_time = time.time()

    degrees = {}
    total_edges = G.numberOfEdges()
    for node in G.iterNodes():
        degree = G.degree(node)
        normalized_degree = degree / total_edges
        degrees[node] = normalized_degree

    end_time = time.time()
    print(f"assign_normalized_degree took {end_time - start_time:.4f} seconds")
    return degrees

def initialize_weights(G: Graph):
    start_time = time.time()

    omega = {}
    uniform_weight = 1.0 / G.numberOfEdges()
    for u, v in G.iterEdges():
        if u < v:
            omega[(u, v)] = uniform_weight
        else:
            omega[(v, u)] = uniform_weight

    end_time = time.time()
    print(f"initialize_weights took {end_time - start_time:.4f} seconds")
    return omega

def WERW_KPath(G: Graph, kappa: int, rho: int, beta: float):
    start_time = time.time()

    normalized_degrees = assign_normalized_degree(G)
    omega = initialize_weights(G)

    for i in range(rho):
        vn = random.choices(list(G.iterNodes()), weights=list(normalized_degrees.values()), k=1)[0]

        MessagePropagation(G, vn, kappa, omega, beta)

    end_time = time.time()
    print(f"WERW_KPath took {end_time - start_time:.4f} seconds")
    return omega

def calculate_probability(G: Graph, current: int, neighbor: int, omega: dict, unvisited_neighbors: list):
    # Calculate the denominator (sum of weights of all unvisited edges)
    denominator = sum(omega.get((min(current, v), max(current, v)), 0) for v in unvisited_neighbors)

    # If denominator is 0, return 0 to avoid division by zero
    if denominator == 0:
        return 0

    # Calculate the weight of the current edge
    edge_weight = omega.get((min(current, neighbor), max(current, neighbor)), 0)

    # Calculate and return the probability
    return edge_weight / denominator

def MessagePropagation(G: Graph, start: int, kappa: int, omega: dict, beta: float):
    start_time = time.time()

    path = [start]
    for _ in range(kappa - 1):  # kappa - 1 perché il nodo di partenza è già nel cammino
        current = path[-1]
        unvisited_neighbors = [v for v in G.iterNeighbors(path[-1]) if v not in path]
        if not unvisited_neighbors:
            break

        edge_probs = [
            calculate_probability(G, current, neighbor, omega, unvisited_neighbors)
            for neighbor in unvisited_neighbors
        ]

        # Choose next node
        next_node = random.choices(unvisited_neighbors, weights=edge_probs, k=1)[0]

        update_edge_weight(omega, path[-1], next_node, beta)
        path.append(next_node)

    end_time = time.time()
    print(f"MessagePropagation took {end_time - start_time:.4f} seconds")

def update_edge_weight(omega: dict, u: int, v: int, beta: float):
    key = (min(u, v), max(u, v))
    omega[key] = omega.get(key, 0) + beta

def werw_centrality_algorithm(G: Graph):
    start_time = time.time()

    kappa = 5  # Maximum path length
    rho = G.numberOfEdges()  # Number of iterations
    beta = 1.0 / G.numberOfEdges()

    omega = WERW_KPath(G, kappa, rho, beta)

    edge_centrality = [(u, v, weight) for (u, v), weight in omega.items()]
    edge_centrality_sorted = sorted(edge_centrality, key=lambda x: x[2], reverse=True)

    end_time = time.time()
    print(f"werw_centrality_algorithm took {end_time - start_time:.4f} seconds")
    return edge_centrality_sorted

def main():
    start_time = time.time()

    # Load graph
    reader = nk.graphio.EdgeListReader(separator=" ", firstNode=0, continuous=False, directed=False)
    G = reader.read("./graph/edges/graph(n=500, m=22400).txt")
    print(f"Grafo caricato. Nodi: {G.numberOfNodes()}, Archi: {G.numberOfEdges()}")

    edge_centrality_sorted = werw_centrality_algorithm(G)

    # Save results to CSV
    csv_data = []
    for u, v, weight in edge_centrality_sorted:
        dict_csv_row = {"edge": f"{u}, {v}", "centrality": weight}
        csv_data.append(dict_csv_row)
    CsvWriter().write(csv_data, "./csv_files/centrality_ERW", ["edge", "centrality"])

    end_time = time.time()
    print(f"main took {end_time - start_time:.4f} seconds")


if __name__ == "__main__":
    main()

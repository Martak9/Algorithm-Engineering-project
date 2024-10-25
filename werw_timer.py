import random
import networkit as nk
from networkit import Graph
from csv_writer import CsvWriter
from collections import defaultdict
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
    start_time = time.time()
    normalized_degrees = assign_normalized_degree(G)
    omega = initialize_weights(G)

    for i in range(rho):
        #if i % 1000 == 0:  # Print progress every 1000 iterations
            #print(f"WERW_KPath progress: {i}/{rho} iterations")
        vn = random.choices(list(G.iterNodes()), weights=list(normalized_degrees.values()), k=1)[0]
        MessagePropagation(G, vn, kappa, omega, beta)

    end_time = time.time()
    #print(f"WERW_KPath execution time: {end_time - start_time:.2f} seconds")
    return omega


def MessagePropagation(G: Graph, start: int, kappa: int, omega: dict, beta: float):
    path = [start]
    visited = set([start])

    for _ in range(kappa - 1):
        current = path[-1]
        neighbors = list(G.iterNeighbors(current))
        unvisited_neighbors = [v for v in neighbors if v not in visited]

        if not unvisited_neighbors:
            break
        start_time = time.time()
        total_weight = sum(omega.get((min(current, v), max(current, v)), 0) for v in unvisited_neighbors)
        end_time = time.time()
        print(f"total_weight {end_time - start_time:.4f} seconds")

        start_time = time.time()
        probs = [omega.get((min(current, v), max(current, v)), 0) / total_weight for v in unvisited_neighbors]
        end_time = time.time()
        print(f"probs {end_time - start_time:.4f} seconds")

        start_time = time.time()
        next_node = random.choices(unvisited_neighbors, weights=probs, k=1)[0]
        end_time = time.time()
        print(f"next_node {end_time - start_time:.4f} seconds")

        edge = (min(current, next_node), max(current, next_node))
        omega[edge] += beta

        path.append(next_node)
        visited.add(next_node)


def werw_centrality_algorithm(G: Graph):
    start_time = time.time()
    kappa = 5  # Maximum path length
    rho = G.numberOfEdges()  # Number of iterations
    beta = 1.0 / G.numberOfEdges()

    omega = WERW_KPath(G, kappa, rho, beta)

    result = sorted(((u, v, weight) for (u, v), weight in omega.items()), key=lambda x: x[2], reverse=True)
    end_time = time.time()
    print(f"werw_centrality_algorithm total execution time: {end_time - start_time:.2f} seconds")
    return result


def main():
    start_time = time.time()
    reader = nk.graphio.EdgeListReader(separator=" ", firstNode=0, continuous=False, directed=False)
    G = reader.read("./graph/edges/graph(n=500, m=44800).txt")
    print(f"Graph loaded. Nodes: {G.numberOfNodes()}, Edges: {G.numberOfEdges()}")

    edge_centrality_sorted = werw_centrality_algorithm(G)

    csv_data = [{"edge": f"{u}, {v}", "centrality": weight} for u, v, weight in edge_centrality_sorted]
    CsvWriter().write(csv_data, "./csv_files/centrality_ERW", ["edge", "centrality"])

    end_time = time.time()
    print(f"Total script execution time: {end_time - start_time:.2f} seconds")


if __name__ == "__main__":
    main()

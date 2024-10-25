import random
import networkit as nk
from networkit import Graph
from csv_writer import CsvWriter


def assign_normalized_degree(G: Graph):
    degrees = {}
    total_nodes = G.numberOfNodes()
    for node in G.iterNodes():
        degree = G.degree(node)
        normalized_degree = degree / total_nodes
        degrees[node] = normalized_degree
    return degrees


def initialize_weights(G: Graph):
    omega = {}
    for u, v in G.iterEdges():
        if u < v:
            omega[(u, v)] = 1
        else:
            omega[(v, u)] = 1
    return omega


def WERW_KPath(G: Graph, kappa: int, rho: int):
    normalized_degrees = assign_normalized_degree(G)
    omega = initialize_weights(G)

    for i in range(rho):
        vn = random.choices(list(G.iterNodes()), weights=list(normalized_degrees.values()), k=1)[0]
        #(f"\nIterazione {i + 1}:")
        #print(f"Nodo di partenza scelto: {vn}")
        MessagePropagation(G, vn, kappa, omega)

        # Debug: #print current weights after each iteration
        #print("Current edge weights:")
        #for edge, weight in omega.items():
            #print(f"Edge {edge}: {weight}")

    # Normalize edge weights
    #print("\nNormalizing weights:")
    for edge in omega:
        omega[edge] /= rho
    #print(f"Edge {edge}: {omega[edge]}")

    return omega


def MessagePropagation(G: Graph, start: int, kappa: int, omega: dict):
    path = [start]
    visited_nodes = set([start])
    #print(f"Cammino: {start}", end="")

    for _ in range(kappa - 1):  # -1 because we start with one node
        current = path[-1]
        unvisited_neighbors = [
            neighbor for neighbor in G.iterNeighbors(current)
            if neighbor not in visited_nodes
        ]

        if not unvisited_neighbors:
           #print(" (terminato: nessun vicino non visitato)")
           break  # No more unvisited neighbors, end the path

        # Calculate probabilities for unvisited neighbors
        edge_probs = [
            calculate_probability(G, current, neighbor, omega, visited_nodes)
            for neighbor in unvisited_neighbors
        ]

        # Choose next node
        next_node = random.choices(unvisited_neighbors, weights=edge_probs, k=1)[0]
        #print(f" -> {next_node}", end="")

        # Update edge weight (only once)
        update_edge_weight(omega, current, next_node)

        # Add to path and mark as visited
        path.append(next_node)
        visited_nodes.add(next_node)

    if len(path) == kappa:
        """#print(" (lunghezza massima raggiunta)")"""
        #print()  # New line after the path


def calculate_probability(G: Graph, vn: int, e: int, omega: dict, visited_nodes: set):
    # Calculate the sum of weights only for unvisited neighbors
    total_weight = sum(get_edge_weight(omega, vn, neighbor)
                       for neighbor in G.iterNeighbors(vn)
                       if neighbor not in visited_nodes)

    # If all neighbors are visited, return 0 to avoid division by zero
    if total_weight == 0:
        return 0

    return get_edge_weight(omega, vn, e) / total_weight


def update_edge_weight(omega: dict, u: int, v: int):
    if u < v:
        omega[(u, v)] += 1
    else:
        omega[(v, u)] += 1


def get_edge_weight(omega: dict, u: int, v: int):
    if u < v:
        return omega.get((u, v), 1)
    else:
        return omega.get((v, u), 1)


def werw_centrality_algorithm(G: Graph):
    kappa = 20  # Maximum path length
    rho = G.numberOfEdges()  # Number of iterations

    omega = WERW_KPath(G, kappa, rho)

    edge_centrality = [(u, v, weight) for (u, v), weight in omega.items()]
    edge_centrality_sorted = sorted(edge_centrality, key=lambda x: x[2], reverse=True)

    return edge_centrality_sorted


def main():
    # Load graph
    reader = nk.graphio.EdgeListReader(separator=" ", firstNode=0, continuous=False, directed=False)
    G = reader.read("./graph/graph(n=4, m=5).txt")
    #print(f"Grafo caricato. Nodi: {G.numberOfNodes()}, Archi: {G.numberOfEdges()}")

    edge_centrality_sorted = werw_centrality_algorithm(G)

    #print("\nFinal Edge Centrality Values (sorted):")
    csv_data = []
    for u, v, weight in edge_centrality_sorted:
        dict_csv_row = {"edge": f"{u}, {v}", "centrality": weight}
        csv_data.append(dict_csv_row)
        #print(f"Edge ({u}, {v}): {weight}")
    CsvWriter().write(csv_data, "./csv_files/centrality_WERW", ["edge", "centrality"])


if __name__ == "__main__":
    main()
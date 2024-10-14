import networkit as nk
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats
import networkx as nx
import time

from erw_kpath_final import erw_centrality_algorithm

print(nk.__version__)

def generate_test_graph(num_nodes, num_edges):
    G = nk.generators.ErdosRenyiGenerator(num_nodes, num_edges).generate()

    weighted_G = nk.Graph(num_nodes, weighted=True, directed=False)  # Grafo pesato
    uniform_weight = 1.0 / G.numberOfEdges()
    for u, v in G.iterEdges():
        weighted_G.addEdge(u, v, uniform_weight)  # Aggiungi l'arco con il peso

    return weighted_G

def edge_betweenness_centrality(G):
    node_betweenness = nk.centrality.Betweenness(G)
    node_betweenness.run()

    return [(u, v, node_betweenness.score(u) + node_betweenness.score(v)) for u, v in G.iterEdges()]

def normalize_centrality(centrality_values):
    min_val = min(cent for _, _, cent in centrality_values)
    max_val = max(cent for _, _, cent in centrality_values)

    if max_val == min_val:
        return [(u, v, 0) for u, v, _ in centrality_values]  # Restituisce zero per tutte le centralità

    return [(u, v, (cent - min_val) / (max_val - min_val)) for u, v, cent in centrality_values]

def compare_rankings(result1, result2):
    sorted_result1 = sorted(result1, key=lambda x: x[2], reverse=True)
    sorted_result2 = sorted(result2, key=lambda x: x[2], reverse=True)

    rank1 = {(u, v): i for i, (u, v, _) in enumerate(sorted_result1)}
    rank2 = {(u, v): i for i, (u, v, _) in enumerate(sorted_result2)}

    edges = list(rank1.keys())
    spearman_corr, _ = stats.spearmanr([rank1[e] for e in edges], [rank2[e] for e in edges])

    return spearman_corr

def run_consistency_test(num_tests, num_nodes, num_edges, num_runs):
    correlations = []
    for i in range(num_tests):
        G = generate_test_graph(num_nodes, num_edges)

        results = [normalize_centrality(erw_centrality_algorithm(G)) for _ in range(num_runs)]

        pair_correlations = []
        for j in range(num_runs):
            for k in range(j + 1, num_runs):
                corr = compare_rankings(results[j], results[k])
                pair_correlations.append(corr)

        avg_correlation = np.mean(pair_correlations)
        correlations.append(avg_correlation)

        print(f"Test {i + 1}: Correlazione media = {avg_correlation:.4f}")

    overall_avg_correlation = np.mean(correlations)
    print(f"\nCorrelazione media complessiva: {overall_avg_correlation:.4f}")
    return overall_avg_correlation > 0.7  # Soglia arbitraria, puoi modificarla

def compare_with_betweenness(num_tests, num_nodes, num_edges, num_runs):
    correlations = []
    for i in range(num_tests):
        G = generate_test_graph(num_nodes, num_edges)

        betweenness = normalize_centrality(edge_betweenness_centrality(G))

        erw_results = [normalize_centrality(erw_centrality_algorithm(G)) for _ in range(num_runs)]

        corrs = [compare_rankings(erw_result, betweenness) for erw_result in erw_results]
        avg_correlation = np.mean(corrs)
        correlations.append(avg_correlation)

        print(f"Test {i + 1}: Correlazione media con Edge Betweenness = {avg_correlation:.4f}")

    overall_avg_correlation = np.mean(correlations)
    print(f"\nCorrelazione media complessiva con Edge Betweenness: {overall_avg_correlation:.4f}")
    return overall_avg_correlation > 0.5  # Soglia arbitraria, puoi modificarla

def visualize_results(G, erw_centrality, betweenness_centrality):
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))

    nx_graph = nx.Graph()
    for u, v in G.iterEdges():
        nx_graph.add_edge(u, v)

    pos = nx.spring_layout(nx_graph)

    nx.draw_networkx_nodes(nx_graph, pos, node_size=10, ax=ax1)
    edge_colors_erw = [erw_centrality.get((u, v), 0) for u, v in G.iterEdges()]
    edges = nx.draw_networkx_edges(nx_graph, pos, edge_color=edge_colors_erw, width=2, ax=ax1)
    ax1.set_title("ERW-Kpath Centrality")
    ax1.axis('off')

    sm1 = plt.cm.ScalarMappable(cmap=plt.cm.viridis, norm=plt.Normalize(vmin=min(edge_colors_erw), vmax=max(edge_colors_erw)))
    sm1.set_array([])
    fig.colorbar(sm1, ax=ax1, label="Centralità")

    nx.draw_networkx_nodes(nx_graph, pos, node_size=10, ax=ax2)
    edge_colors_betweenness = [betweenness_centrality.get((u, v), 0) for u, v in G.iterEdges()]
    edges = nx.draw_networkx_edges(nx_graph, pos, edge_color=edge_colors_betweenness, width=2, ax=ax2)
    ax2.set_title("Edge Betweenness Centrality")
    ax2.axis('off')

    sm2 = plt.cm.ScalarMappable(cmap=plt.cm.viridis, norm=plt.Normalize(vmin=min(edge_colors_betweenness), vmax=max(edge_colors_betweenness)))
    sm2.set_array([])
    fig.colorbar(sm2, ax=ax2, label="Centralità")

    plt.tight_layout()
    plt.show()

num_tests = 1
num_nodes = 5
num_edges = 8
num_runs = 3

print("Test di consistenza:")
if run_consistency_test(num_tests, num_nodes, num_edges, num_runs):
    print("L'algoritmo ERW-Kpath mostra una buona consistenza tra diverse esecuzioni.")
else:
    print("L'algoritmo ERW-Kpath mostra una bassa consistenza tra diverse esecuzioni.")

print("\nConfronto con Edge Betweenness:")
if compare_with_betweenness(num_tests, num_nodes, num_edges, num_runs):
    print("L'algoritmo ERW-Kpath mostra una correlazione significativa con Edge Betweenness Centrality.")
else:
    print("L'algoritmo ERW-Kpath mostra una bassa correlazione con Edge Betweenness Centrality.")

G = generate_test_graph(num_nodes, num_edges)

erw_centrality = {(u, v): cent for u, v, cent in normalize_centrality(erw_centrality_algorithm(G))}
betweenness_centrality = {(u, v): cent for u, v, cent in normalize_centrality(edge_betweenness_centrality(G))}


visualize_results(G, erw_centrality, betweenness_centrality)

plt.show()
time.sleep(10)


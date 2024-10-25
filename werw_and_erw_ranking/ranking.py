import os
from datetime import datetime
import networkit as nk
from tests.werw_test import werw_centrality_algorithm
from erw_kpath_final import erw_centrality_algorithm
import csv
import pandas as pd
import matplotlib.pyplot as plt



def get_file_name(base_name, extension, directory, index):
    return os.path.join(directory, f"{base_name}_{index}.{extension}")


def read_results(filename):
    results = {}
    with open(filename, 'r') as f:
        for line in f:
            u, v, centrality = map(float, line.strip().split())
            edge = (int(u), int(v))
            results[edge] = float(centrality)
    return results


def werw_results(G, output_file):
    results = werw_centrality_algorithm(G)
    edge_centralities = {(u, v): centrality for u, v, centrality in results}
    save_results(G, edge_centralities, output_file)
    return edge_centralities


def erw_results(G, output_file):
    results = erw_centrality_algorithm(G)
    edge_centralities = {(u, v): centrality for u, v, centrality in results}
    save_results(G, edge_centralities, output_file)
    return edge_centralities


def save_results(G, edge_centralities, output_file):
    with open(output_file, 'w') as f:
        for u, v in G.iterEdges():
            centrality = edge_centralities.get((u, v), edge_centralities.get((v, u), 0))
            f.write(f"{u} {v} {centrality}\n")


def calculate_edge_distances(results1, results2):
    edges = sorted(set(results1.keys()) | set(results2.keys()))
    distances = []
    for i, edge in enumerate(edges):
        pos1 = i
        pos2 = i
        if edge in results1:
            pos1 = list(results1.keys()).index(edge)
        if edge in results2:
            pos2 = list(results2.keys()).index(edge)
        distance = abs(pos1 - pos2)
        distances.append((*edge, distance))
    return distances


def calculate_average_distance(distances):
    if len(distances) == 0:
        return 0
    total_distance = sum(distance for _, _, distance in distances)
    average_distance = total_distance / len(distances)
    return average_distance


def run_full_test(test_number, directory):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_directory = os.path.join("werw_and_erw_ranking/results_albert", f"test_results_{timestamp}_k=20")
    os.makedirs(output_directory, exist_ok=True)

    reader = nk.graphio.EdgeListReader(separator=" ", firstNode=0, continuous=False, directed=False)
    G = reader.read("graph/albert/Albert(n=20480, m=102380).txt")

    total_average_distances = {
        "werw_erw": 0
    }

    csv_output_file = os.path.join(output_directory, "distance_results.csv")

    with open(csv_output_file, 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(['Test', 'WERW-ERW'])

    for i in range(1, test_number + 1):
        erw_output_file = get_file_name("erw_results", "txt", output_directory, i)
        werw_output_file = get_file_name("werw_results", "txt", output_directory, i)

        werw_res = werw_results(G, werw_output_file)
        erw_res = erw_results(G, erw_output_file)

        distances_werw_erw = calculate_edge_distances(werw_res, erw_res)

        average_distance_werw_erw = calculate_average_distance(distances_werw_erw)

        total_average_distances["werw_erw"] += average_distance_werw_erw

        print(f"Test {i} completed. Average distance WERW-ERW: {average_distance_werw_erw}")

        with open(csv_output_file, 'a', newline='') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow([f"Test {i}", average_distance_werw_erw])

    overall_average_distances = {
        comparison: total / test_number
        for comparison, total in total_average_distances.items()
    }

    with open(csv_output_file, 'a', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow([])
        csvwriter.writerow(['Overall Average', overall_average_distances["werw_erw"]])

    show_csv_as_table(csv_output_file, "Test results: k=20, n=20480, m=102380", output_directory)

    print(f"Overall average distance WERW-ERW: {overall_average_distances['werw_erw']}")


def show_csv_as_table(csv_file, title, save_directory):
    df = pd.read_csv(csv_file)
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.axis('tight')
    ax.axis('off')
    table = ax.table(cellText=df.values, colLabels=df.columns, cellLoc='center', loc='center')
    plt.title(title, fontsize=14, pad=20)
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.scale(1.2, 1.2)
    plt.show()
    output_file_path = os.path.join(save_directory, f"{title.replace(' ', '_')}.png")
    fig.savefig(output_file_path, bbox_inches='tight')
    print(f"Table saved as {output_file_path}")


if __name__ == "__main__":
    number_of_tests = 10
    output_directory = os.path.abspath("results")
    run_full_test(number_of_tests, output_directory)
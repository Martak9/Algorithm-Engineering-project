import os
import json
import time
import networkit as nk
import matplotlib.pyplot as plt
from werw_test import werw_centrality_algorithm
from erw_kpath_final import erw_centrality_algorithm
from tabulate import tabulate  # Assicurati di installare questa libreria con pip install tabulate

def load_config(config_file_name="./doubling_experiment_config.json"):
    with open(config_file_name, 'r') as file:
        config = json.load(file)
    return config

def filter_graph_files(config, keyword=""):
    result = []
    graph_dir = config["graph"]["graphs_dir"]
    subfolders = config["graph"]["subfolders"]

    for subfolder in subfolders:
        subfolder_path = os.path.join(graph_dir, subfolder)
        if not os.path.exists(subfolder_path):
            print(f"Sottocartella {subfolder} non trovata.")
            continue
        for file in os.listdir(subfolder_path):
            file_path = os.path.join(subfolder_path, file)
            result.append(file_path)
    return result

def create_log_directory(config):
    log_dir = os.path.join(config["log"]["log_directory"], time.strftime("%Y%m%d-%H%M%S"))
    os.makedirs(log_dir, exist_ok=True)
    return log_dir

def run_test(config):
    repetition = config["repetition"]
    log_dir = create_log_directory(config)

    algorithms = {
        "WERW": werw_centrality_algorithm,
        "ERW": erw_centrality_algorithm
    }

    file_list = filter_graph_files(config)
    results = {alg: {file: [] for file in file_list} for alg in algorithms}
    edge_counts = {alg: {file: [] for file in file_list} for alg in algorithms}

    for file in file_list:
        print(f"\n{'=' * 50}")
        print(f"Esecuzione su file: {file}")
        print(f"{'=' * 50}")

        for alg_name, algorithm in algorithms.items():
            print(f"\n{'-' * 30}")
            print(f"Algoritmo: {alg_name}")
            print(f"{'-' * 30}")

            alg_log_dir = os.path.join(log_dir, alg_name, os.path.basename(file).split('.')[0])
            os.makedirs(alg_log_dir, exist_ok=True)

            for i in range(repetition):
                print(f"\nTest {i + 1}/{repetition}")

                reader = nk.graphio.EdgeListReader(separator=" ", firstNode=0, continuous=False, directed=False)
                graph = reader.read(file)
                start_time = time.time()

                result = algorithm(graph)

                end_time = time.time()
                execution_time = end_time - start_time

                print(f"Tempo di esecuzione: {execution_time:.2f} secondi")

                results[alg_name][file].append(execution_time)
                edge_counts[alg_name][file].append(graph.numberOfEdges())

                log_file_path = os.path.join(alg_log_dir, f"execution_{i + 1}.log")
                with open(log_file_path, "w") as log_file:
                    log_file.write(f"Esecuzione {i + 1}/{repetition} per {file} con {alg_name}:\n")
                    log_file.write(f"Tempo di esecuzione: {execution_time:.2f} secondi\n")
                    log_file.write(f"Risultato: {result}\n")

    create_execution_time_graphs(results, edge_counts, log_dir)
    create_results_table(results, edge_counts, log_dir)

def create_execution_time_graphs(results, edge_counts, log_dir):
    plt.figure(figsize=(12, 6))

    for alg_name in results.keys():
        data_points = []

        for file in results[alg_name].keys():
            avg_execution_time = sum(results[alg_name][file]) / len(results[alg_name][file])
            avg_edge_count = edge_counts[alg_name][file][0]
            data_points.append((avg_edge_count, avg_execution_time))

        data_points.sort(key=lambda x: x[0])

        x_data, y_data = zip(*data_points)

        plt.scatter(x_data, y_data, label=alg_name)
        plt.plot(x_data, y_data, marker='o')

    plt.title('Tempo di esecuzione in base al numero di archi')
    plt.xlabel('Numero di archi')
    plt.ylabel('Tempo di esecuzione (secondi)')
    plt.legend()
    plt.grid(True)

    graph_path = os.path.join(log_dir, "execution_time_vs_edges.png")
    plt.savefig(graph_path)
    plt.close()

def create_results_table(results, edge_counts, log_dir):
    table_data = []
    for alg_name in results.keys():
        for file in results[alg_name].keys():
            avg_execution_time = sum(results[alg_name][file]) / len(results[alg_name][file])
            avg_edge_count = edge_counts[alg_name][file][0]
            table_data.append([alg_name, os.path.basename(file), avg_edge_count, f"{avg_execution_time:.2f}"])

    headers = ["Algoritmo", "Grafo", "Numero di archi", "Tempo medio di esecuzione (s)"]
    table = tabulate(table_data, headers=headers, tablefmt="grid")

    table_path = os.path.join(log_dir, "results_table.txt")
    with open(table_path, "w") as f:
        f.write(table)

    print("\nTabella dei risultati:")
    print(table)

if __name__ == "__main__":
    configurazione = load_config()
    run_test(configurazione)
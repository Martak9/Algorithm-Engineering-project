import networkit as nk
import numpy as np
import subprocess
import time
import os

from werw_kpath_final import werw_centrality_algorithm



def run_jar_algorithm(jar_path, input_file, output_file, k_path_length=5, delimiter=" "):
    command = [
        'java', '-Xmx4G', '-jar', jar_path, input_file, output_file, str(k_path_length), delimiter
    ]
    print(f"Executing command: {' '.join(command)}")
    try:
        result = subprocess.run(command, check=True, capture_output=True, text=True)
        print("JAR Output:")
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Error executing JAR: {e}")
        print("JAR Output:")
        print(e.stdout)
        print("JAR Error:")
        print(e.stderr)
        raise


def read_sorted_results(filename):
    results = []
    with open(filename, 'r') as f:
        for line in f:
            u, v, centrality = map(float, line.strip().split())
            results.append((int(u), int(v), centrality))
    return sorted(results, key=lambda x: x[2], reverse=True)


def your_algorithm(G, output_file):
    results = werw_centrality_algorithm(G)
    with open(output_file, 'w') as f:
        for u, v, centrality in results:
            f.write(f"{u} {v} {centrality}\n")
    return results


def compare_results(your_results, jar_results):
    max_diff = 0
    for i, ((u1, v1, cent1), (u2, v2, cent2)) in enumerate(zip(your_results, jar_results)):
        if (u1, v1) != (u2, v2):
            print(f"Warning: Edge mismatch at position {i}. Your algorithm: ({u1}, {v1}), JAR: ({u2}, {v2})")
        diff = abs(cent1 - cent2)
        max_diff = max(max_diff, diff)
    return max_diff


def run_correctness_test(num_tests, num_nodes, num_edges, jar_path):
    for i in range(num_tests):
        print(f"Test {i + 1}/{num_tests}")

        input_file = f"./graph/edges/2expedge(n=500, m=700).txt"
        print(f"Input file saved: {input_file}")

        reader = nk.graphio.EdgeListReader(separator=" ", firstNode=0, continuous=False, directed=False)
        G = reader.read("./graph/edges/2expedge(n=500, m=700).txt")
        # Print the contents of the input file
        print("Input file contents:")
        with open(input_file, 'r') as f:
            print(f.read())

        # Esegui il tuo algoritmo e salva i risultati ordinati
        your_output_file = f"./your_results_{i}.txt"
        your_results = your_algorithm(G, your_output_file)
        print(f"Your algorithm results saved: {your_output_file}")

        # Esegui l'algoritmo del file JAR
        jar_output_file = os.path.abspath(f"jar_results_{i}.txt")
        try:
            run_jar_algorithm(jar_path, input_file, jar_output_file)
            print(f"JAR results saved: {jar_output_file}")

            # Leggi i risultati ordinati del JAR
            jar_results = read_sorted_results(jar_output_file)
            print(jar_results)

            # Confronta i risultati
            max_difference = compare_results(your_results, jar_results)

            print(f"  Massima differenza: {max_difference}")

            # Puoi impostare una soglia di tolleranza, ad esempio 1e-6
            if max_difference < 1e-6:
                print("  Test superato!")
            else:
                print("  Test fallito. Le differenze sono troppo grandi.")
        except Exception as e:
            print(f"Error during test {i + 1}: {e}")



        print()


# Parametri di test
num_tests = 1
num_nodes = 10
num_edges = 30
jar_path = "./werw_kpath_trusted/werw-kpath.jar"

run_correctness_test(num_tests, num_nodes, num_edges, jar_path)
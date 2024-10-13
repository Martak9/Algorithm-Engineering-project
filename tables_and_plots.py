import re
import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from prettytable import PrettyTable



# Funzione per estrarre i dati dal testo
def extract_data(text):
    data = []
    lines = text.split('\n')
    for i, line in enumerate(lines):
        if line.startswith('Esecuzione'):
            match = re.search(r'Esecuzione (\d+)/(\d+) per (.+) con (.+):', line)
            if match:
                execution, total_executions, graph, algorithm = match.groups()
                if i + 1 < len(lines):
                    time_match = re.search(r'Tempo di esecuzione: (\d+\.\d+) secondi', lines[i + 1])
                    if time_match:
                        time = float(time_match.group(1))
                        data.append({
                            'Execution': int(execution),
                            'Graph': graph.split('/')[-1],
                            'Algorithm': algorithm,
                            'Time': time
                        })
    return pd.DataFrame(data)


# Funzione per estrarre i risultati degli algoritmi
def extract_results(text):
    results = []
    current_graph = ''
    current_algorithm = ''
    for line in text.split('\n'):
        if line.startswith('Esecuzione'):
            match = re.search(r'Esecuzione (\d+)/(\d+) per (.+) con (.+):', line)
            if match:
                current_graph = match.group(3).split('/')[-1]
                current_algorithm = match.group(4)
        elif line.startswith('Risultato:'):
            result = eval(line.split(':', 1)[1].strip())
            for edge in result:
                results.append({
                    'Graph': current_graph,
                    'Algorithm': current_algorithm,
                    'Edge': f'{edge[0]}-{edge[1]}',
                    'Weight': edge[2]
                })
    return pd.DataFrame(results)


# Leggi il contenuto del file
file_path = os.path.join('./', 'log.txt')
with open(file_path, 'r') as file:
    content = file.read()

# Estrarre i dati
df = extract_data(content)

if df.empty:
    print("Nessun dato estratto dal file. Verifica il contenuto del file di log.")
else:
    # Creare una tabella riassuntiva
    summary = df.groupby(['Graph', 'Algorithm'])['Time'].agg(['mean', 'min', 'max']).reset_index()
    summary = summary.round(4)

    # Creare e visualizzare la tabella usando PrettyTable
    table = PrettyTable()
    table.field_names = ["Graph", "Algorithm", "Mean Time", "Min Time", "Max Time"]
    for _, row in summary.iterrows():
        table.add_row([row['Graph'], row['Algorithm'], row['mean'], row['min'], row['max']])
    print("Tabella riassuntiva dei tempi di esecuzione:")
    print(table)

    # Creare un grafico a linee per l'andamento dei tempi di esecuzione
    plt.figure(figsize=(12, 6))
    for algorithm in df['Algorithm'].unique():
        algorithm_data = df[df['Algorithm'] == algorithm].groupby('Graph')['Time'].mean().reset_index()
        plt.plot(algorithm_data['Graph'], algorithm_data['Time'], marker='o', label=algorithm)

    plt.title('Andamento dei tempi di esecuzione per Grafo e Algoritmo')
    plt.xlabel('Grafo')
    plt.ylabel('Tempo medio di esecuzione (secondi)')
    plt.legend(title='Algoritmo')
    plt.xticks(rotation=45)
    plt.tight_layout()

    # Mostrare il grafico senza salvarlo su file
    plt.show()

    # Creare un grafico a barre per i tempi di esecuzione
    plt.figure(figsize=(12, 6))
    sns.barplot(x='Graph', y='Time', hue='Algorithm', data=df)
    plt.title('Tempi di esecuzione per Grafo e Algoritmo')
    plt.xlabel('Grafo')
    plt.ylabel('Tempo di esecuzione (secondi)')
    plt.xticks(rotation=45)
    plt.tight_layout()

    # Mostrare il grafico senza salvarlo su file
    plt.show()

    # Estrarre i risultati
    results_df = extract_results(content)

    # Creare un grafico a dispersione per i pesi degli archi
    for graph in results_df['Graph'].unique():
        plt.figure(figsize=(12, 6))
        graph_data = results_df[results_df['Graph'] == graph]
        sns.scatterplot(x='Edge', y='Weight', hue='Algorithm', data=graph_data)
        plt.title(f'Pesi degli archi per il grafo {graph}')
        plt.xlabel('Arco')
        plt.ylabel('Peso')
        plt.xticks(rotation=90)
        plt.legend(title='Algoritmo')
        plt.tight_layout()

        # Mostrare il grafico senza salvarlo su file
        plt.show()

    print("Visualizzazioni create con successo!")

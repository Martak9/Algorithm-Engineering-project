import os

# Definisci la cartella principale e la sottocartella che ti interessa
cartella_principale = 'graph'  # Sostituisci con il percorso corretto
sottocartella = 'albert'  # Sostituisci con il nome della sottocartella che vuoi modificare

# Crea il percorso completo della sottocartella
percorso_sottocartella = os.path.join(cartella_principale, sottocartella)

# Scorri tutti i file nella sottocartella specificata
for nome_file in os.listdir(percorso_sottocartella):
    file_path = os.path.join(percorso_sottocartella, nome_file)
    
    # Verifica che sia effettivamente un file
    if os.path.isfile(file_path):
        # Leggi il file corrente e scrivi le modifiche in un nuovo file con "_mod" aggiunto al nome
        with open(file_path, 'r') as f_in:
            with open(f"{file_path}_mod", 'w') as f_out:
                for line in f_in:
                    nodo1, nodo2 = line.split()
                    # Aggiungi il peso 1 e scrivi nel nuovo file
                    f_out.write(f"{nodo1} {nodo2} 1\n")

        print(f"Modificato: {file_path}")

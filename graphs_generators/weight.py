import os


cartella_principale = 'graph'  
sottocartella = 'albert'  

percorso_sottocartella = os.path.join(cartella_principale, sottocartella)

for nome_file in os.listdir(percorso_sottocartella):
    file_path = os.path.join(percorso_sottocartella, nome_file)
    
    if os.path.isfile(file_path):
        with open(file_path, 'r') as f_in:
            with open(f"{file_path}_mod", 'w') as f_out:
                for line in f_in:
                    nodo1, nodo2 = line.split()
                    f_out.write(f"{nodo1} {nodo2} 1\n")

        print(f"Modificato: {file_path}")

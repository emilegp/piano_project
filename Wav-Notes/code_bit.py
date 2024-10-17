import json
import os
import numpy as np

# Charger le fichier JSON avec votre signal
input_filepath = 'Wav-Notes/notes_dict_1ligne.json'
with open(input_filepath, 'r') as f:
    data = json.load(f)

# Obtenir le répertoire du fichier original
output_directory = os.path.dirname(input_filepath)

# Fonction pour réduire la précision d'un signal en fonction du nombre de bits
def reduce_precision(signal, n_bits):
    if n_bits == 1:
        # Cas spécial pour 1 bit : toutes les valeurs négatives deviennent 0
        return [1 if value > 0 else 0 for value in signal]
    elif n_bits > 1:
        levels = 2**(n_bits - 1)  # Utiliser n_bits - 1 pour tenir compte du bit de signe
        # Quantifier le signal dans le nombre de niveaux approprié
        signal_quantified = np.round(np.array(signal) * (levels // 2)) / (levels // 2)
    else:
        signal_quantified = np.zeros_like(signal)  # Tout est ramené à zéro pour 0 bit
    
    return signal_quantified.tolist()  # Convertir en liste pour garder le format JSON

# Fonction pour créer un nouveau fichier JSON pour chaque niveau de bits
def create_modified_json(data, n_bits, output_directory):
    # Créer un nouveau dictionnaire avec les signaux modifiés
    modified_data = {}
    
    for note, vecteurs in data.items():
        modified_data[note] = [reduce_precision(vecteur, n_bits) for vecteur in vecteurs]
    
    # Générer le nom de fichier pour chaque niveau de bits
    output_filename = os.path.join(output_directory, f'modified_signal_{n_bits}bit.json')
    
    # Sauvegarder le nouveau dictionnaire dans un fichier JSON
    with open(output_filename, 'w') as outfile:
        json.dump(modified_data, outfile, indent=4)

# Créer un fichier JSON pour chaque niveau de bits dans le même répertoire que le fichier original
create_modified_json(data, 16, output_directory)
create_modified_json(data, 8, output_directory)
create_modified_json(data, 6, output_directory)
create_modified_json(data, 4, output_directory)
create_modified_json(data, 3, output_directory)
create_modified_json(data, 2, output_directory)
create_modified_json(data, 1, output_directory)
create_modified_json(data, 0, output_directory)
import numpy as np
import matplotlib.pyplot as plt
import json
import os
from scipy.optimize import curve_fit

# Charger le fichier JSON
with open('C:/Users/maxim/OneDrive/Documents/GitHub/piano_project/Wav-Notes/notes_dict_1ligne.json', 'r') as f:
    data = json.load(f)
input_filepath = 'Wav-Notes/notes_dict_1ligne.json'
# Obtenir le répertoire du fichier original
output_directory = os.path.dirname(input_filepath)

# Paramètres à ajustés
#filtre_bas = [100,100,150,150,200,200,250,250,300,300,350,350,400,400,500,500]
#filtre_haut = [2000,1500,2000,1500,2000,1500,2000,1500,2000,1500,2000,1500,2000,1500,2000,1500]
filtre_bas=[1]
filtre_haut=[10000]
redu=114 #facteur de Réduction de la fréquence d'échantillonnage

# Paramètres importants
fs = int(44100//redu)  # sample rate
dt = 0.1  # Intervalle de temps (en secondes)
nb_recordings = 1  # nb d'enregistrements par note
nb_points = int(dt * fs)  # Équivalent en nombre de points pour les indices
point_du_tap = 11 # Sert à l'affichage

notes= ['1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17']
notes_matrix = np.zeros((len(notes) * nb_recordings, nb_points))

# Transférer les données du dictionnaire dans une matrice avec 17 lignes et nb_points par ligne
i = 0
for note, recordings in data.items():
    for prise in recordings:
        array = np.array(prise)
        array_fin=array[::redu]
        if len(array_fin)!=nb_points:
            array_fin=array_fin[:nb_points]
        notes_matrix[i] = array_fin
        i += 1

def dico_filtré_passband(matrice, frequence_minimale, frequence_maximale):
    # 1. Effectuer la transformée de Fourier rapide (FFT)
    signal_fft = np.fft.rfft(matrice)
    frequencies = np.fft.rfftfreq(len(matrice[0]), 1/fs)

    # 2. Créer un filtre passe-bande
    low_cutoff = frequence_minimale  # Fréquence de coupure basse (Hz)
    high_cutoff = frequence_maximale  # Fréquence de coupure haute (Hz)
    filter_mask = (frequencies > low_cutoff) & (frequencies < high_cutoff)

    # 3. Appliquer le filtre
    filtered_fft = signal_fft * filter_mask

    # 4. Revenir au domaine temporel avec la transformée inverse de Fourier
    filtered_signal = np.fft.irfft(filtered_fft)
    
    # 5. Remplacer la deuxième moitié de chaque vecteur par des zéros
    filtered_signal_cut = np.zeros_like(filtered_signal)  # Créer une matrice du même type, remplie de zéros
    half_point = filtered_signal.shape[1] // 2  # Obtenir le point de coupure (moitié)
    filtered_signal_cut[:, :half_point] = filtered_signal[:, :half_point]
    
    # Retourne le nouveau dico avec les signaux filtrés
    return filtered_signal_cut, frequencies, filtered_fft[point_du_tap], signal_fft[point_du_tap]

def create_modified_json(fbas, fhaut, freq_sampling, output_directory):
    for bas, haut in zip(fbas, fhaut):
        # Appliquer les filtres à la matrice
        matrice_traitee, frequencies, filtered_fft, signal_fft = dico_filtré_passband(notes_matrix, bas, haut)

        # Créer un dictionnaire pour cette combinaison de filtres
        notes_dict = {}
        
        for i, note in enumerate(notes):
            recordings = []
            for j in range(nb_recordings):
                # Convertir en liste chaque enregistrement traité
                recordings.append(matrice_traitee[i * nb_recordings + j].tolist())
            notes_dict[note] = recordings

        # Générer un fichier JSON pour chaque combinaison de filtre
        output_filename = os.path.join(output_directory, f'fs={freq_sampling}-fbas={bas}-fhaut={haut}.json')

        # Sauvegarder ce dictionnaire dans un fichier JSON
        with open(output_filename, 'w') as outfile:
            json.dump(notes_dict, outfile, indent=4)


# Créer un fichier JSON pour chaque niveau de bits dans le même répertoire que le fichier original
create_modified_json(filtre_bas, filtre_haut, fs, output_directory)

#La suite du code n'est pas utile en soit mais permet de confirmer que ça donne la bonne chose AND IT DOES!!
sign, frequencies, filtered_fft, signal_fft=dico_filtré_passband(notes_matrix,filtre_bas[0],filtre_haut[0])
signal_post_filtre=sign[point_du_tap]
signal=notes_matrix[point_du_tap]

# Générer le temps 
t1 = np.linspace(0, 1, len(signal), endpoint=False)  # Intervalle de temps
t2 = np.linspace(0, 1, len(signal_post_filtre), endpoint=False)  # Intervalle de temps
#f1, f2 = 50, 200  # Fréquences des sinusoïdes
#signal = np.sin(2 * np.pi * f1 * t) + 0.5 * np.sin(2 * np.pi * f2 * t)

# Afficher les résultats
plt.figure(figsize=(10, 6))

# Affichage du signal original
plt.subplot(2, 2, 1)
plt.plot(t1, signal)
plt.title("Signal original")
plt.xlabel("Temps [s]")
plt.ylabel("Amplitude")

# Spectre de fréquence original
plt.subplot(2, 2, 2)
plt.plot(frequencies[:fs//2], np.abs(signal_fft)[:fs//2])
plt.title("Spectre de fréquence original")
plt.xlabel("Fréquence [Hz]")
plt.ylabel("Amplitude")

# Spectre de fréquence filtré
plt.subplot(2, 2, 4)
plt.plot(frequencies[:fs//2], np.abs(filtered_fft)[:fs//2])
plt.title("Spectre de fréquence filtré")
plt.xlabel("Fréquence [Hz]")
plt.ylabel("Amplitude")

# Signal filtré
plt.subplot(2, 2, 3)
plt.plot(t2, signal_post_filtre.real)
plt.title("Signal filtré")
plt.xlabel("Temps [s]")
plt.ylabel("Amplitude")

plt.tight_layout()
plt.show()
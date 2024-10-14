import numpy as np
import matplotlib.pyplot as plt
import json
from scipy.optimize import curve_fit

# Charger le fichier JSON
with open('C:/Users/maxim/OneDrive/Documents/GitHub/piano_project/Wav-Notes/notes_dict_on_god.json', 'r') as f:
    data = json.load(f)

# Paramètres importants
fs = 44100  # sample rate
dt = 0.1  # Intervalle de temps (en secondes)
nb_recordings = 20  # nb d'enregistrements par note
nb_points = int(dt * fs)  # Équivalent en nombre de points pour les indices
point_du_tap = 130

notes = ['c3', 'c-3', 'd3', 'd-3', 'e3', 'f3', 'f-3', 'g3', 'g-3', 'a3', 'a-3', 'b3']
notes_matrix = np.zeros((len(notes) * nb_recordings, nb_points))

# Transférer les données du dictionnaire dans une matrice avec 12*nb_recordings lignes et nb_points par ligne
i = 0
for note, recordings in data.items():
    for prise in recordings:
        array = np.array(prise)
        notes_matrix[i] = array
        i += 1

def dico_filtré_passband(frequence_minimale, frequence_maximale):
    # 1. Effectuer la transformée de Fourier rapide (FFT)
    signal_fft = np.fft.rfft(notes_matrix)
    frequencies = np.fft.rfftfreq(len(notes_matrix[0]), 1/fs)

    # 2. Créer un filtre passe-bande
    low_cutoff = frequence_minimale  # Fréquence de coupure basse (Hz)
    high_cutoff = frequence_maximale  # Fréquence de coupure haute (Hz)
    filter_mask = (frequencies > low_cutoff) & (frequencies < high_cutoff)

    # 3. Appliquer le filtre
    filtered_fft = signal_fft * filter_mask

    # 4. Revenir au domaine temporel avec la transformée inverse de Fourier
    filtered_signal = np.fft.irfft(filtered_fft)

    # Retourne le nouveau dico avec les signaux filtrés
    return filtered_signal, frequencies, filtered_fft[point_du_tap], signal_fft[point_du_tap]

#La suite du code n'est pas utile en soit mais permet de confirmer que ça donne la bonne chose AND IT DOES!!
sign, frequencies, filtered_fft, signal_fft=dico_filtré_passband(150,3000)
filtered_signal=sign[point_du_tap]
signal=notes_matrix[point_du_tap]

# Générer le temps 
freqs = int(fs*dt)  # Fréquence d'échantillonnage (Hz)
t = np.linspace(0, 1, freqs, endpoint=False)  # Intervalle de temps
#f1, f2 = 50, 200  # Fréquences des sinusoïdes
#signal = np.sin(2 * np.pi * f1 * t) + 0.5 * np.sin(2 * np.pi * f2 * t)

# Afficher les résultats
plt.figure(figsize=(10, 6))

# Affichage du signal original
plt.subplot(2, 2, 1)
plt.plot(t, signal)
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
plt.plot(t, filtered_signal.real)
plt.title("Signal filtré")
plt.xlabel("Temps [s]")
plt.ylabel("Amplitude")

plt.tight_layout()
plt.show()


import numpy as np
import matplotlib.pyplot as plt
import json
from scipy.optimize import curve_fit

# Charger le fichier JSON
with open('C:/Users/maxim/OneDrive/Documents/GitHub/piano_project/Wav-Notes/notes_dict_on_god.json', 'r') as f:
    data = json.load(f)

# Charger le fichier JSON
with open('C:/Users/maxim/OneDrive/Documents/GitHub/piano_project/Wav-Notes/dico_bit/modified_signal_1bit.json', 'r') as f:
    data1bit = json.load(f)

# Fonction gaussienne
def gaussian(x, a, mu, sigma):
    return a * np.exp(-((x - mu) ** 2) / (2 * sigma ** 2))

# Fonction pour faire la corrélation pour un dico donné
def corr(nom_du_dico, tap):
    # Paramètres importants
    fs = 44100  # sample rate
    dt = 0.1  # Intervalle de temps (en secondes)
    nb_recordings = 20  # nb d'enregistrements par note
    nb_points = int(dt * fs)  # Équivalent en nombre de points pour les indices
    point_du_tap = tap

    notes = ['c3', 'c-3', 'd3', 'd-3', 'e3', 'f3', 'f-3', 'g3', 'g-3', 'a3', 'a-3', 'b3']
    notes_matrix = np.zeros((len(notes) * nb_recordings, nb_points))

    # Transférer les données du dictionnaire dans une matrice avec 12*nb_recordings lignes et nb_points par ligne
    i = 0
    for note, recordings in nom_du_dico.items():
        for prise in recordings:
            array = np.array(prise)
            notes_matrix[i] = array
            i += 1

    # Produit scalaire (corrélation) entre un point et les 240 autres points
    scalar_prod = np.dot(notes_matrix, notes_matrix[point_du_tap])
    maximum = np.max(np.abs(scalar_prod))
    correlation = scalar_prod / maximum

    return correlation

# Fonction pour ajuster la courbe gaussienne (Pur chatGPT)
def fit_gaussian(corr_data):
    x_data = np.arange(len(corr_data))  # Générer les indices comme x
    initial_guess = [1, np.argmax(corr_data), 1]  # Estimation initiale (amplitude, centre, largeur)
    
    # Ajustement de la courbe gaussienne
    params, _ = curve_fit(gaussian, x_data, corr_data, p0=initial_guess)
    
    return params, x_data

# Tracer les corrélations avec ajustement gaussien (Pur chatGPT)
def plot_corr_and_gaussian(corr_data, title):
    params, x_data = fit_gaussian(corr_data)
    
    # Extraire les paramètres ajustés
    amplitude_fit, mean_fit, sigma_fit = params
    
    # Générer la courbe ajustée
    y_fit = gaussian(x_data, amplitude_fit, mean_fit, sigma_fit)

    # Tracer les données et la courbe ajustée
    plt.figure(figsize=(12, 6))
    plt.plot(corr_data, label='Corrélation', color='red')
    plt.plot(x_data, y_fit, label='Fit Gaussien', color='blue', linestyle='--')

    plt.title(title)
    plt.xlabel("Indice")
    plt.ylabel("Amplitude")
    plt.legend()
    plt.show()

# Corrélation et affichage pour les données originales
corr_data_original = corr(data, 120)
plot_corr_and_gaussian(corr_data_original, "Signal original")

# Corrélation et affichage pour les données 2-bit
corr_data_1bit = corr(data1bit, 120)
plot_corr_and_gaussian(corr_data_1bit, "Signal abîmé")


# Générer un signal de test (somme de deux sinusoïdes)
fs = 1000  # Fréquence d'échantillonnage (Hz)
t = np.linspace(0, 1, fs, endpoint=False)  # Intervalle de temps
f1, f2 = 50, 200  # Fréquences des sinusoïdes
signal = np.sin(2 * np.pi * f1 * t) + 0.5 * np.sin(2 * np.pi * f2 * t)

# 1. Effectuer la transformée de Fourier rapide (FFT)
signal_fft = np.fft.fft(signal)
frequencies = np.fft.fftfreq(len(signal), 1/fs)

# 2. Créer un filtre passe-bande
low_cutoff = 40  # Fréquence de coupure basse (Hz)
high_cutoff = 100  # Fréquence de coupure haute (Hz)
filter_mask = (np.abs(frequencies) > low_cutoff) & (np.abs(frequencies) < high_cutoff)

# 3. Appliquer le filtre
filtered_fft = signal_fft * filter_mask

# 4. Revenir au domaine temporel avec la transformée inverse de Fourier
filtered_signal = np.fft.ifft(filtered_fft)

# Afficher les résultats
plt.figure(figsize=(12, 6))

# Affichage du signal original
plt.subplot(3, 1, 1)
plt.plot(t, signal)
plt.title("Signal original")
plt.xlabel("Temps [s]")
plt.ylabel("Amplitude")

# Spectre de fréquence original
plt.subplot(3, 1, 2)
plt.plot(frequencies[:fs//2], np.abs(signal_fft)[:fs//2])
plt.title("Spectre de fréquence original")
plt.xlabel("Fréquence [Hz]")
plt.ylabel("Amplitude")

# Signal filtré
plt.subplot(3, 1, 3)
plt.plot(t, filtered_signal.real)
plt.title("Signal filtré")
plt.xlabel("Temps [s]")
plt.ylabel("Amplitude")

plt.tight_layout()
plt.show()

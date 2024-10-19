import numpy as np
import matplotlib.pyplot as plt
import json
from scipy.optimize import curve_fit


# Fonction pour calculer la corrélation
def corr(nom_du_dico, tap):
    nb_points = len(nom_du_dico['1'][0])  
    dt = 0.1
    fs=int(nb_points/dt) # sample rate
    nb_recordings = 1
    point_du_tap = tap

    notes = ['1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17']
    notes_matrix = np.zeros((len(notes) * nb_recordings, nb_points))

    i = 0
    for note, recordings in nom_du_dico.items():
        for prise in recordings:
            array = np.array(prise)
            array_normalise = array / np.max(array)
            notes_matrix[i] = array_normalise
            i += 1

    scalar_prod = np.dot(notes_matrix, notes_matrix[point_du_tap])
    maximum = np.max(np.abs(scalar_prod))
    correlation = scalar_prod / maximum

    return correlation

#Listes de dicos:
fichiers=['fs=44100-fbas=100-fhaut=1500','fs=1764-fbas=100-fhaut=1500',
    'fs=882-fbas=100-fhaut=1500','fs=44100-fbas=300-fhaut=1500','fs=1764-fbas=300-fhaut=1500',
    'fs=1470-fbas=300-fhaut=1500','fs=882-fbas=300-fhaut=1500',
    'fs=44100-fbas=300-fhaut=5000','fs=4410-fbas=300-fhaut=5000',
    'fs=2205-fbas=300-fhaut=5000','fs=2004-fbas=300-fhaut=5000',
    'fs=1764-fbas=300-fhaut=5000','fs=1575-fbas=300-fhaut=5000',
    'fs=1470-fbas=300-fhaut=5000','fs=4410-fbas=550-fhaut=1500',
    'fs=44100-fbas=550-fhaut=1500','fs=1470-fbas=550-fhaut=1500',
    'fs=44100-fbas=1000-fhaut=5000','fs=8820-fbas=1000-fhaut=5000',
    'fs=44100-fbas=700-fhaut=3000','fs=4410-fbas=700-fhaut=3000',
    'fs=1917-fbas=700-fhaut=3000','fs=1837-fbas=700-fhaut=3000',
    'fs=1764-fbas=700-fhaut=3000','fs=1696-fbas=700-fhaut=3000',
    'fs=1633-fbas=700-fhaut=3000']
#1-6

fichiers=['notes_dict_1ligne','modified_signal_1bit','modified_signal_2bit','modified_signal_3bit'
          ,'modified_signal_4bit','modified_signal_6bit','modified_signal_8bit','modified_signal_16bit']
#nb_bit

fichiers=['fs=44100-fbas=100-fhaut=1500','fs=1764-fbas=100-fhaut=1500',
    'fs=882-fbas=100-fhaut=1500','fs=44100-fbas=300-fhaut=1500','fs=1764-fbas=300-fhaut=1500',
    'fs=1470-fbas=300-fhaut=1500','fs=882-fbas=300-fhaut=1500']
#1-2
fichiers=['fs=44100-fbas=300-fhaut=5000','fs=4410-fbas=300-fhaut=5000',
    'fs=2205-fbas=300-fhaut=5000','fs=2004-fbas=300-fhaut=5000',
    'fs=1764-fbas=300-fhaut=5000','fs=1575-fbas=300-fhaut=5000',
    'fs=1470-fbas=300-fhaut=5000','fs=4410-fbas=550-fhaut=1500',
    'fs=44100-fbas=550-fhaut=1500','fs=1470-fbas=550-fhaut=1500']
#3-4
fichiers=['fs=44100-fbas=1000-fhaut=5000','fs=8820-fbas=1000-fhaut=5000',
    'fs=44100-fbas=700-fhaut=3000','fs=4410-fbas=700-fhaut=3000',
    'fs=1917-fbas=700-fhaut=3000','fs=1837-fbas=700-fhaut=3000',
    'fs=1764-fbas=700-fhaut=3000','fs=1696-fbas=700-fhaut=3000',
    'fs=1633-fbas=700-fhaut=3000']
#5-6


# Ajustement avec plancher, incertitudes et bornes
#def fit_gaussian_with_offset_and_errors(corr_data, yerr):
# x_data = np.arange(len(corr_data))
# initial_guess = [1, np.argmax(corr_data), 1, np.mean(corr_data)]  # [amplitude, mean, sigma, offset]

# # Ajuster les bornes de l'offset : autoriser des valeurs autour de la moyenne des données
# offset_mean = np.mean(corr_data)
# bounds = ([0, 0, 0, offset_mean - 0.01], [1, len(corr_data), np.inf, offset_mean + 0.01])  

# # Utilisation des erreurs dans l'ajustement
# params, pcov = curve_fit(gaussian_with_offset, x_data, corr_data, p0=initial_guess, 
#                             sigma=yerr, absolute_sigma=True, bounds=bounds, maxfev=10000)

# perr = np.sqrt(np.diag(pcov))  # Erreurs sur les paramètres ajustés
# return params, perr, x_data

# Fonction pour obtenir la résolution et le contraste
#def analyze_gaussian_fit(corr_data, yerr):
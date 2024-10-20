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
fichiers=['fs=44100-fbas=300-fhaut=1000','fs=44100-fbas=300-fhaut=1500',
    'fs=44100-fbas=300-fhaut=1750','fs=44100-fbas=300-fhaut=2250','fs=44100-fbas=300-fhaut=3000',
    'fs=44100-fbas=300-fhaut=5000','fs=4410-fbas=300-fhaut=1000','fs=4410-fbas=300-fhaut=1500',
    'fs=4410-fbas=300-fhaut=1750','fs=4410-fbas=300-fhaut=2250','fs=4410-fbas=300-fhaut=3000',
    'fs=4410-fbas=300-fhaut=5000','fs=2004-fbas=300-fhaut=1000','fs=2004-fbas=300-fhaut=1500',
    'fs=2004-fbas=300-fhaut=1750','fs=2004-fbas=300-fhaut=2250','fs=2004-fbas=300-fhaut=3000',
    'fs=2004-fbas=300-fhaut=5000','fs=1002-fbas=300-fhaut=1000','fs=1002-fbas=300-fhaut=1500',
    'fs=1002-fbas=300-fhaut=1750','fs=1002-fbas=300-fhaut=2250','fs=1002-fbas=300-fhaut=3000',
    'fs=1002-fbas=300-fhaut=5000']
#Marielou-Nyquist

# Fonction gaussienne pour curve_fit
def gaussian_with_floor(x, A, mu, sigma, floor):
    return A * np.exp(-((x - mu) ** 2) / (2 * sigma ** 2)) + floor

# Fonction pour ajuster avec des bornes (curve_fit)
def fit_gaussian_with_bounds(corr_data, xaxis, yerr):
    x_data = xaxis  # np.arange(len(corr_data))
    initial_guess = [np.max(corr_data), np.argmax(corr_data), np.std(corr_data), np.mean(corr_data)]  # [amplitude, mean, sigma, offset]

    # Contraintes sur les bornes pour que sigma > 0 et floor proche de la moyenne des données
    bounds = ([0, 0, 0, np.mean(corr_data) - 0.09], [np.inf, len(corr_data), np.inf, np.mean(corr_data) + 0.09])

    # Utilisation de curve_fit avec la nouvelle fonction gaussienne
    params, pcov = curve_fit(gaussian_with_floor, x_data, corr_data, p0=initial_guess,
                             sigma=yerr, absolute_sigma=True, bounds=bounds, maxfev=10000)

    perr = np.sqrt(np.diag(pcov))  # Erreurs sur les paramètres ajustés
    return params, perr, x_data

# Fonction pour calculer la corrélation du curve_fit
def correlateur_et_curve_fit_gaussien(data, point_du_tap):
        #Rembarque sur le code à Marielou
    # Paramètres importants
    nb_points = len(data['1'][0])  
    dt = 0.1
    fs=int(nb_points/dt) # sample rate
    nb_recordings = 1  # nb d'enregistrements par note

    notes = ['1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17']
    matrice = np.zeros((len(notes) * nb_recordings, nb_points))

    i = 0
    for note, recordings in data.items():
        for prise in recordings:
            array = np.array(prise)
            array_normalise = array / np.max(array)
            matrice[i] = array_normalise
            i += 1

    signaux_reference = matrice
    signal = matrice[point_du_tap]
    position = 3*10**(-2) + 1.5*np.arange(0, 17)*10**(-2)
    correlation = np.dot(signaux_reference,signal)/np.max(np.dot(signaux_reference,signal))

    nb_bits = 32
    range = 2
    err_ampl = (range/(2**(nb_bits)))/2

    # Propagation de l'erreur sur le produit scalaire de la corrélation
    yerr = []
    for element in signaux_reference:
        # Remplacer les zéros par une petite valeur pour éviter la division par zéro
        signal_safe = np.where(signal == 0, 1e-10, signal)
        element_safe = np.where(element == 0, 1e-10, element)

        # Calculer l'erreur de multiplication
        err_multiplication = (signal_safe * element_safe) * np.sqrt((err_ampl / signal_safe) ** 2 + (err_ampl / element_safe) ** 2)

        # Vérifier si err_multiplication contient des NaN ou des infinis
        if np.any(np.isnan(err_multiplication)) or np.any(np.isinf(err_multiplication)):
            print("Attention : err_multiplication contient des NaN ou des infinis.")
            continue  # Passer à l'itération suivante

        # Calculer l'erreur totale
        err_prod = np.sqrt(np.sum(err_multiplication ** 2))
        yerr.append(err_prod)
    #yerr=1*correlation

    params, perr, x_data = fit_gaussian_with_bounds(correlation,position, yerr)
    
    amplitude_fit, mean_fit, sigma_fit, offset_fit = params
    amplitude_err, mean_err, sigma_err, offset_err = perr

    # La résolution est convertie en cm (chaque point est espacé de 1,5 cm)
    resolution = 1.5 * np.log(2) * np.sqrt(2) * sigma_fit
    resolution_err = 1.5 * np.log(2) * np.sqrt(2) * sigma_err

    max_diff = amplitude_fit-offset_fit
    max_diff_err = amplitude_err-offset_err

    return {
        "resolution": resolution,
        "resolution_err": resolution_err,
        "max_diff": max_diff,
        "max_diff_err": max_diff_err,
    }


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
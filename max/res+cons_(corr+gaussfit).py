import numpy as np
import json
import pandas as pd
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
print('Librairies importées')


fichiers=['notes_dict_1ligne','modified_signal_1bit','modified_signal_2bit','modified_signal_3bit'
          ,'modified_signal_4bit','modified_signal_6bit','modified_signal_8bit','modified_signal_16bit'
          ,'fs=8820-fbas=300-fhaut=1500']
#Ajouter les futurs dicos à corréler

# Charger les fichiers JSON
def lecteur():
    encyclopedie=[]
    for nom in fichiers:
        with open(f'Wav-Notes/{nom}.json', 'r') as f:
            encyclopedie.append(json.load(f))
    return encyclopedie 

# Fonction gaussienne avec plancher
def gaussian_with_offset(x, a, mu, sigma, offset):
    return a * np.exp(-((x - mu) ** 2) / (2 * sigma ** 2)) + offset

# Fonction pour calculer la corrélation
def corr(nom_du_dico, tap):
    nb_points = len(nom_du_dico['1'][0])  # sample rate
    dt = 0.1
    fs=int(nb_points/dt)
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

# Ajustement avec plancher, incertitudes et bornes
def fit_gaussian_with_offset_and_errors(corr_data, yerr):
    x_data = np.arange(len(corr_data))
    initial_guess = [1, np.argmax(corr_data), 1, np.mean(corr_data)]  # [amplitude, mean, sigma, offset]
    
    # Ajuster les bornes de l'offset : autoriser des valeurs autour de la moyenne des données
    offset_mean = np.mean(corr_data)
    bounds = ([0, 0, 0, offset_mean - 0.01], [1, len(corr_data), np.inf, offset_mean + 0.01])  

    # Utilisation des erreurs dans l'ajustement
    params, pcov = curve_fit(gaussian_with_offset, x_data, corr_data, p0=initial_guess, 
                             sigma=yerr, absolute_sigma=True, bounds=bounds, maxfev=10000)
    
    perr = np.sqrt(np.diag(pcov))  # Erreurs sur les paramètres ajustés
    return params, perr, x_data

# Fonction pour obtenir la résolution et le contraste
def analyze_gaussian_fit(corr_data, yerr):
    # Ajuster les données avec la fonction gaussienne avec plancher
    params, perr, x_data = fit_gaussian_with_offset_and_errors(corr_data, yerr)
    
    # Extraction des paramètres ajustés
    amplitude_fit, mean_fit, sigma_fit, offset_fit = params
    amplitude_err, mean_err, sigma_err, offset_err = perr

    # La résolution est convertie en cm (chaque point est espacé de 1,5cm)
    resolution = 1.5 * np.log(2) * np.sqrt(2) * sigma_fit
    resolution_err = 1.5 * np.log(2) * np.sqrt(2) * sigma_err  

    # Calcul de la différence entre le maximum de la gaussienne et l'offset
    max_diff = amplitude_fit
    max_diff_err = amplitude_err  # Incertitude sur la différence est celle de l'amplitude

    # Retourner les résultats
    return {
        "resolution": resolution,
        "resolution_err": resolution_err,
        "max_diff": max_diff,
        "max_diff_err": max_diff_err,
    }

# Créer une liste pour stocker les résultats
results_list = []

# Liste des dictionnaires à traiter
dictionaries_to_process = lecteur()  # Ajoute les autres dictionnaires ici

# Liste des noms correspondant aux dictionnaires
bit_names = ['Original', '1bit', '2bit', '3bit', '4bit', '6bit', '8bit', '16bit']

for idx, current_data in enumerate(dictionaries_to_process):
    a1 = []
    a2 = []
    a3 = []
    a4 = []
    for i in range(6):
        corr_data = corr(current_data, 3 + 2 * i)
        vec_norm = corr_data / np.max(corr_data)
        
        # Incertitudes fictives pour l'exemple (à remplacer par les vraies valeurs)
        yerr = np.random.uniform(0.05, 0.15, size=len(vec_norm))
                
        # Analyser les ajustements
        results = analyze_gaussian_fit(vec_norm, yerr)
        a1.append(results["resolution"])
        a2.append(results["resolution_err"])
        a3.append(results["max_diff"])
        a4.append(results["max_diff_err"])

    resolution = np.mean(a1)
    resolution_err = np.mean(a2)
    contraste = np.mean(a3)
    contraste_err = np.mean(a4)

    # Ajouter les résultats à la liste, en incluant les noms des bits
    results_list.append({
        "Dictionnaire": bit_names[idx],
        "Résolution": resolution,
        "Erreur Résolution": resolution_err,
        "Contraste": contraste,
        "Erreur Contraste": contraste_err,
    })

# Convertir les résultats en DataFrame
results_df = pd.DataFrame(results_list)

# Exporter les résultats en fichier Excel
results_df.to_excel('resultats_analyses.xlsx', index=False)

print("Analyse terminée et résultats exportés vers 'resultats_analyses.xlsx'.")

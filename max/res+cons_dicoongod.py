import numpy as np
from scipy.odr import ODR, Model, RealData
import json
import pandas as pd
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
print('Librairies importées')



fichiers=['notes_dict_1ligne']

# Charger les fichiers JSON
def lecteur():
    encyclopedie=[]
    for nom in fichiers:
        with open(f'Wav-Notes/{nom}.json', 'r') as f:
            encyclopedie.append(json.load(f))
    return encyclopedie 

# Fonction gaussienne pour curve_fit
def gaussian_with_floor(x, A, mu, sigma, floor):
    return A * np.exp(-((x - mu) ** 2) / (2 * sigma ** 2)) + floor

# Fonction pour ajuster avec des bornes (curve_fit)
def fit_gaussian_with_bounds(corr_data, xaxis, yerr):
    x_data = xaxis  # np.arange(len(corr_data))
    initial_guess = [np.max(corr_data), np.argmax(corr_data), np.std(corr_data), np.mean(corr_data)]  # [amplitude, mean, sigma, offset]

    # Contraintes sur les bornes pour que sigma > 0 et floor proche de la moyenne des données
    bounds = ([0, 0, 0, np.mean(corr_data) - 0.01], [np.inf, len(corr_data), np.inf, np.mean(corr_data) + 0.01])

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
    nb_recordings = 20  # nb d'enregistrements par note

    notes= ['c3','c-3','d3','d-3','e3','f3','f-3','g3','g-3','a3','a-3','b3']
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
    correlation_bloc = np.dot(signaux_reference,signal)/np.max(np.dot(signaux_reference,signal))
    correlation= np.mean(correlation_bloc.reshape(-1, nb_recordings), axis=1)

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



# Fonction gaussienne ODR
def gaussian_with_floor_constrained(p, x):
    A, mu, log_sigma, floor = p
    sigma = np.exp(log_sigma)  # σ > 0 en utilisant la transformation exponentielle
    return A * np.exp(-((x - mu) ** 2) / (2 * sigma ** 2)) + floor

# Fonction pour calculer la corrélation ODR
def correlateur_ODR(data,point_du_tap,nb_bit):
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

    nb_bits = nb_bit
    range = 2
    err_ampl = (range/(2**(nb_bits)))/2
    err_position = 4e-3

    # Propagation de l'erreur sur le produit scalaire de la corrélation
    err_prod_ampl = []
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
        err_prod_ampl.append(err_prod)

    # Utilisation de ODR pour faire le fit gaussien avec σ toujours positif
    data = RealData(position, correlation, sx=err_position, sy=err_prod_ampl)
    model = Model(gaussian_with_floor_constrained)
    
    guess_initial = [np.max(correlation), np.mean(position), np.log(np.std(position)), np.mean(correlation)]
    odr = ODR(data, model, beta0=guess_initial)
    output = odr.run()

    # Paramètres optimaux et matrice de covariance
    A_opt, mu_opt, log_sigma_opt, floor_opt = output.beta
    sigma_opt = np.exp(log_sigma_opt)  # Revenir à σ

    # Calculer la gaussienne ajustée
    #gaussian_fit = gaussian_with_floor_constrained([A_opt, mu_opt, log_sigma_opt, floor_opt], position)
    #
    # # Afficher les résultats
    # plt.figure(figsize=(10, 6))
    # plt.plot(position, correlation, 'bo', label="Données originales")
    # plt.plot(position, gaussian_fit, 'r-', label="Ajustement gaussien")
    # plt.title("Ajustement d'une gaussienne aux données")
    # plt.xlabel("Position [m]")
    # plt.ylabel("Amplitude")
    # plt.legend()
    # plt.grid(True)
    # plt.show()

    resolution = np.sqrt(2 * np.log(2)) * sigma_opt
    resolution_err = np.sqrt(2 * np.log(2)) * sigma_opt * np.sqrt(output.cov_beta[2, 2])

    contraste = A_opt-np.mean(correlation)
    contraste_err = 2*np.sqrt(output.cov_beta[0, 0])
    
    return {
        "resolution": resolution,
        "resolution_err": resolution_err,
        "max_diff": contraste,
        "max_diff_err": contraste_err,
    }

# Ajustement avec plancher, incertitudes et bornes
#def fit_gaussian_with_offset_and_errors(corr_data, yerr):
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
#def analyze_gaussian_fit(corr_data, yerr):
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
dictionaries_to_process = lecteur()  # Ajoute les autres dictionnaires ici
bit_names = fichiers #['Original', '1bit', '2bit', '3bit', '4bit', '6bit', '8bit', '16bit']
bit_qty=[32,1,2,3,4,6,8,16] #bit_qty[idx]

for idx, current_data in enumerate(dictionaries_to_process):
    a1 = []
    a2 = []
    a3 = []
    a4 = []
    for i in range(6):
        corr_data = correlateur_ODR(current_data, 3 + 2 * i,32)

        # Analyser les ajustements
        results = corr_data
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
results_df.to_excel('resultats_dicoongod.xlsx', index=False)

print("Analyse terminée et résultats exportés vers 'resultats_ODRcontraste=A-f.xlsx'.")

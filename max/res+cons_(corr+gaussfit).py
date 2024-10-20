import numpy as np
from scipy.odr import ODR, Model, RealData
import json
import pandas as pd
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
print('Librairies importées')

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

# Charger les fichiers JSON
def lecteur():
    encyclopedie=[]
    for nom in fichiers:
        with open(f'Wav-Notes/{nom}.json', 'r') as f:
            encyclopedie.append(json.load(f))
    return encyclopedie 

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

    #Calculer la gaussienne ajustée
    #gaussian_fit = gaussian_with_floor_constrained([A_opt, mu_opt, log_sigma_opt, floor_opt], position)
    
    # print(A_opt-np.mean(correlation))
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
    for i in [7,8,9,10,11]:
        corr_data = correlateur_ODR(current_data, i,32)

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
results_df.to_excel('resultats_nouveaux_points_confirm.xlsx', index=False)

print("Analyse terminée et résultats exportés vers 'nyquist'.")

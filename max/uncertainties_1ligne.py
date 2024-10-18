import numpy as np
from scipy.odr import ODR, Model, RealData
import matplotlib.pyplot as plt
import json


# Fonction gaussienne
def gaussian_with_floor(p, x):
    A, mu, sigma, floor = p
    return A * np.exp(-((x - mu) ** 2) / (2 * sigma ** 2)) + floor

# Set-up des arrays et des erreurs (à changer pour les vraies valeurs)
with open('Wav-Notes/notes_dict_1ligne.json', 'r') as f:
    data = json.load(f)


def correlateur(data,point_du_tap,nb_bit):
    #Rembarque sur le code à Marielou
    # Paramètres importants
    fs = int(44100)  # sample rate
    dt = 0.1  # Intervalle de temps (en secondes)
    nb_recordings = 1  # nb d'enregistrements par note
    nb_points = int(dt * fs)  # Équivalent en nombre de points pour les indices
#    nb_points = len(data['1'][0])  # sample rate   

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


    # Utilisation de ODR pour faire le fit gaussien (permet d'avoir des incertitudes en x et y), trouvé avec ChatGPT
    data = RealData(position, correlation, sx=err_position, sy=err_prod_ampl)
    model = Model(gaussian_with_floor)
    guess_initial = [np.max(correlation), np.mean(position), np.std(position), np.mean(correlation)]  # Ajuster mu et sigma
    odr = ODR(data, model, beta0=guess_initial)
    output = odr.run()

    # Paramètres optimaux et matrice de covariance
    A_opt, mu_opt, sigma_opt, floor_opt = output.beta
    cov_matrix = output.cov_beta

    # Trouver l'incertitude sur la résolution
    resolution = np.sqrt(2*np.log(2)) * sigma_opt
    sigma_err = np.sqrt(cov_matrix[2, 2])  
    resolution_err = np.sqrt(2*np.log(2)) * sigma_err

    # Trouver l'incertitude sur le contraste
    contraste = A_opt
    contraste_err = np.sqrt(cov_matrix[0, 0])  

    return contraste, contraste_err, resolution, resolution_err

# print(A_opt, floor_opt)
# gaussian=gaussian_with_floor(output.beta, position)
# plt.plot(position, gaussian)
# plt.plot(position, correlation)
# plt.show()

# print(f'Résolution: ', FWHM, '+-', FWHM_err)
# print(f'Contraste: ', contraste, '+-', contraste_err)

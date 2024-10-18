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

# Paramètres importants
redu=1 #facteur de Réduction de la fréquence d'échantillonnage
fs = int(44100//redu)  # sample rate
dt = 0.1  # Intervalle de temps (en secondes)
nb_recordings = 1  # nb d'enregistrements par note
nb_points = int(dt * fs)  # Équivalent en nombre de points pour les indices
point_du_tap = 11

notes= ['1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17']
notes_matrix = np.zeros((len(notes), nb_points))

# Transférer les données du dictionnaire dans une matrice avec 12*nb_recordings lignes et nb_points par ligne
i = 0
for note, recordings in data.items():
    for prise in recordings:
        array = np.array(prise)
        array_fin=array[::redu]
        notes_matrix[i] = array_fin
        i += 1

#Rembarque sur le code à Marielou
signaux_reference = notes_matrix
signal = notes_matrix[point_du_tap]
position = (3 + 1.5*point_du_tap) * (10**(-2))
correlation = np.dot(signaux_reference,signal)

nb_bits = 32
range = 1
err_ampl = (range/(2**(nb_bits)))/2
err_position = 4e-3

# Propagation de l'erreur sur le produit scalaire de la corrélation
err_prod_ampl=[]
for element in signaux_reference:
    err_multiplication = (signal*element)*np.sqrt((err_ampl/signal)**2+(err_ampl/element)**2)
    err_prod = np.sqrt(np.sum(err_multiplication**2))
    err_prod_ampl.append(err_prod)


# Utilisation de ODR pour faire le fit gaussien (permet d'avoir des incertitudes en x et y), trouvé avec ChatGPT
data = RealData(position, correlation, sx=err_position, sy=err_prod_ampl)

model = Model(gaussian_with_floor)

guess_initial = [np.max(correlation), 2, 2, np.min(correlation)]  # Changer les guess de sigma et mu

odr = ODR(data, model, beta0=guess_initial)

output = odr.run()

# Paramètres optimaux et matrice de covariance
A_opt, mu_opt, sigma_opt, floor_opt = output.beta
cov_matrix = output.cov_beta

# Trouver l'incertitude sur la résolution
FWHM = np.sqrt(2*np.log(2)) * sigma_opt
sigma_err = np.sqrt(cov_matrix[2, 2])  
FWHM_err = np.sqrt(2*np.log(2)) * sigma_err

# Trouver l'incertitude sur le contraste
contraste = A_opt
contraste_err = np.sqrt(cov_matrix[0, 0])  

print(A_opt, floor_opt)
gaussian=gaussian_with_floor(output.beta, position)
plt.plot(position, gaussian)
plt.show()

print(f'Résolution: ', FWHM, '+-', FWHM_err)
print(f'Contraste: ', contraste, '+-', contraste_err)

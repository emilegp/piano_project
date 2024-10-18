import numpy as np
from scipy.odr import ODR, Model, RealData

# Fonction gaussienne
def gaussian_model(p, x):
    A, mu, sigma = p
    return A * np.exp(-(x - mu)**2 / (2 * sigma**2))

# Set-up des arrays et des erreurs (à changer pour les vraies valeurs)
signaux_reference = np.array([[2,3,4,1,3,2,4],[1,2,3,4,3,2,1],[3,2,1,4,3,1,2],[4,1,2,3,1,2,1]])
signal = np.array([1,2,3,4,3,2,1])
position = np.array([1,2,3,4])
correlation = np.dot(signaux_reference,signal)

nb_bits=32
range=1
err_ampl=(range/(2**(nb_bits)))/2
err_position= 4e-3

# Propagation de l'erreur sur le produit scalaire de la corrélation
err_prod_ampl=[]
for element in signaux_reference:
    err_multiplication=(signal*element)*np.sqrt((err_ampl/signal)**2+(err_ampl/element)**2)
    print(err_multiplication)
    err_prod=np.sqrt(np.sum(err_multiplication**2))
    err_prod_ampl.append(err_prod)
print(err_prod_ampl)


# Utilisation de ODR pour faire le fit gaussien (permet d'avoir des incertitudes en x et y), trouvé avec ChatGPT
data = RealData(position, correlation, sx=err_position, sy=err_prod_ampl)

model = Model(gaussian_model)

guess_initial = [np.max(correlation), 2, 2]

odr = ODR(data, model, beta0=guess_initial)

output = odr.run()

# Paramètres optimaux et matrice de covariance
A_opt, mu_opt, sigma_opt = output.beta
cov_matrix = output.cov_beta

# Trouver l'incertitude sur la FWHM
FWHM = np.sqrt(2*np.log(2)) * sigma_opt
sigma_uncertainty = np.sqrt(cov_matrix[2, 2])  
FWHM_uncertainty = np.sqrt(2*np.log(2)) * sigma_uncertainty

print(FWHM_uncertainty)

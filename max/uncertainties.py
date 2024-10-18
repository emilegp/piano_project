import numpy as np
from scipy.odr import ODR, Model, RealData
import matplotlib.pyplot as plt

# Fonction gaussienne
def gaussian_with_floor(p, x):
    A, mu, sigma, floor = p
    return A * np.exp(-((x - mu) ** 2) / (2 * sigma ** 2)) + floor

# Set-up des arrays et des erreurs (à changer pour les vraies valeurs)
signaux_reference = np.array([[2,3,4,1,3,2,4],[1,2,3,4,3,2,1],[3,2,1,4,3,1,2],[4,1,2,3,1,2,1]])
signal = np.array([1,2,3,4,3,2,1])
position = np.array([1,2,3,4])
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

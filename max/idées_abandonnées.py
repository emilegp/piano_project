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


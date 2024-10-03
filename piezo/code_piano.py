import sounddevice as sd
import matplotlib.pyplot as plt
import numpy as np
import json
import math

#Ouvrir le training
with open('piezo\\notes_dict.json', 'r') as file:
    data = json.load(file)

fs = 44100 #sample rate
seconds = 1 #temps d'enregistrement
dt = 0.1  #Intervalle de temps (en secondes)
nb_recordings=5 #nb d'enregistrements par note
nb_points= int(dt*fs) #Équivalent en nombre de points pour les indices

notes= ['c3','c-3','d3','d-3','e3','f3','f-3','g3','g-3','a3','a-3','b3']
notes_matrix=np.zeros((len(notes)*nb_recordings, nb_points)) 

#Transférer les données du dictionnaire dans une matrice avec 12*nb_recordings lignes et nb_points par ligne
i=0
for note, recordings in data.items():
    for element in recordings:
        array = np.array(element) 
        notes_matrix[i]=array
        i+=1

#Enregistrement du signal test
default = True #Si cette option est utilisée, le micro/speaker par défaut est utilisé
devices = sd.query_devices()

if not default:
    InputStr = "Choisir le # correspondant au micro parmis la liste: \n"
    OutputStr = "Choisir le # correspondant au speaker parmis la liste: \n"
    for i in range(len(devices)):
        if devices[i]['max_input_channels']:
            InputStr += ('%d : %s \n' % (i, ''.join(devices[i]['name'])))
        if devices[i]['max_output_channels']:
            OutputStr += ('%d : %s \n' % (i, ''.join(devices[i]['name'])))
    DeviceIn = input(InputStr)
    DeviceOut = input(OutputStr)

    sd.default.device = [int(DeviceIn), int(DeviceOut)]


print(f'Enregistrement de la note')

myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels= 1)
sd.wait()
print(f'Enregistrement fini.')

#Trouver l'amplitude maximale en valeur absolue
max_amplitude = np.max(abs(myrecording))
threshold = max_amplitude / 10  #Définir le seuil

#Créer la fenêtre utilisée pour le signal
for index,value in enumerate(myrecording):
    if value>=threshold:
        start_signal=index
        break
cut_signal=myrecording[start_signal:(start_signal+nb_points)].flatten()

#Normalisation du signal
norm_cut_signal=cut_signal/max_amplitude

#Transformer la liste en array
signal_array=np.array(norm_cut_signal)

#Produit scalaire (corrélation) entre les données de training et le signal test
scalar_prod=np.dot(notes_matrix,signal_array)
print(scalar_prod)

#Trouver l'indice de la valeur max du produit scalaire et trouver sa note correspondante
index_max=np.argmax(np.max(scalar_prod))
note_index=math.ceil(index_max/nb_recordings)

print(f"La note à jouer est:",notes[note_index])




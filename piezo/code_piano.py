import sounddevice as sd
import matplotlib.pyplot as plt
import numpy as np

data = np.loadtxt('piezo\\recordings.csv', delimiter=',', dtype=str)
recordings = data[:, :].astype(float)

notes= ['c3','c-3','d3','d-3','e3','f3','f-3','g3','g-3','a3','a-3','b3']

seconds = 5 
fs = 44100      # Sampling rate    

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

dt = 5e-2  #Intervalle de temps (en secondes)
nb_points= int(dt*fs) #Équivalent en nombre de points pour les indices

print(f'Enregistrement de la note')

myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels= 1)
sd.wait()
print(f'Enregistrement fini.')

#Trouver l'amplitude maximale en valeur absolue
max_amplitude = np.max(abs(myrecording))
threshold = max_amplitude / 20  #Définir le seuil

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

correlation=[]
for note in recordings:
    scalar_prod=np.dot(signal_array,note)
    correlation.append(scalar_prod)

correlation_norm=correlation/np.max(correlation).astype(float)

index_max=np.argmax(correlation_norm)

print(f"La note à jouer est:",notes[index_max])




import sounddevice as sd
import matplotlib.pyplot as plt
import numpy as np

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

recordings = []
notes= ['c3','c-3','d3','d-3','e3','f3','f-3','g3','g-3','a3','a-3','b3']
dt = 5e-2  #Intervalle de temps (en secondes)
nb_points= int(dt*fs) #Équivalent en nombre de points pour les indices

for note in notes:
    print(f'Enregistrement de la note',note)

    myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels= 1)
    sd.wait()
    print(f'Enregistrement fini.')

    #Trouver l'amplitude maximale en valeur absolue
    max_amplitude = np.max(abs(myrecording))
    threshold = max_amplitude / 10  #Définir le seuil
    print(threshold)

    #Créer la fenêtre utilisée pour le signal
 
    for index,value in enumerate(myrecording):
        if value>=threshold:
            start_signal=index
            break

    cut_signal=myrecording[start_signal:(start_signal+nb_points)].flatten()

    #Normalisation du signal
    norm_cut_signal=cut_signal/max_amplitude

    t = np.linspace(0,dt,nb_points)
    t2 = np.arange(0,5,1/44100)
    print(len(norm_cut_signal))
    print(len(t))

    plt.plot(t, norm_cut_signal)
    plt.xlabel('Temps [s]')
    plt.ylabel('Amplitude')
    plt.show()

    
    plt.plot(t2, myrecording)
    plt.xlabel('Temps [s]')
    plt.ylabel('Amplitude')
    plt.show()

    #Rajouter le nouveau array à la liste 'recordings'
    recordings.append(norm_cut_signal)

#Transformer la liste en array
recordings_array=np.array(recordings)
print(recordings_array)


#Enregistrer un fichier csv
np.savetxt('kwave\\reverse_runs\\recordings.csv', recordings_array, delimiter=',')
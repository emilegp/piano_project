import sounddevice as sd
import numpy as np
import json

seconds = 2 
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

notes= ['c3','c-3','d3','d-3','e3','f3','f-3','g3','g-3','a3','a-3','b3', 'easter']
#notes= ['c3','c-3','d3']

notes_dict = {note: None for note in notes}
#print(notes_dict)
dt = 1e-1  #Intervalle de temps (en secondes)
nb_points= int(dt*fs) #Équivalent en nombre de points pour les indices

for note in notes:
    recordings=[]
    for i in range(20):
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

        #Rajouter le nouveau array à la liste 'recordings'
        recordings.append(norm_cut_signal.tolist())

    #Transformer la liste en array
    nom_note=note
    notes_dict[nom_note]=recordings

    # t = np.linspace(0,dt,nb_points)
    # t2 = np.arange(0,5,1/44100)

    # plt.plot(t, norm_cut_signal)
    # plt.xlabel('Temps [s]')
    # plt.ylabel('Amplitude')
    # plt.show()

    
    # plt.plot(t2, myrecording)
    # plt.xlabel('Temps [s]')
    # plt.ylabel('Amplitude')
    # plt.show()  

# Save to a JSON file
with open('notes_dict.json', 'w') as json_file:
    json.dump(notes_dict, json_file)

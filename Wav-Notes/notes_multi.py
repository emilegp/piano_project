import sounddevice as sd
import numpy as np
import threading
import matplotlib.pyplot as plt
import time
from collections import deque
import pygame
from pydub import AudioSegment
import os# Parameters
import json
import math

with open('notes_dict_on_god.json', 'r') as file:
    data = json.load(file)

fs = 44100 
dt = 0.1  #Intervalle de temps (en secondes)
nb_recordings=20
nb_points= int(dt*fs)

notes= ['c3','c-3','d3','d-3','e3','f3','f-3','g3','g-3','a3','a-3','b3']
notes_matrix=np.zeros((len(notes)*nb_recordings, nb_points))

# Convert the data for each note into numpy arrays and append to the list
i=0
for note, recordings in data.items():
    for element in recordings:
        array = np.array(element) 
        notes_matrix[i]=array
        i+=1

notes_dict = {
    'c3': 'c3.wav',
    'c-3': 'c-3.wav',
    'd3': 'd3.wav',
    'd-3': 'd-3.wav',
    'e3': 'e3.wav',
    'f3': 'f3.wav',
    'f-3': 'f-3.wav',
    'g3': 'g3.wav',
    'g-3': 'g-3.wav',
    'a3': 'a4.wav',
    'a-3': 'a-4.wav',
    'b3': 'b4.wav'
}

# Initialize pygame mixer
pygame.mixer.init()

# Function to play a note (runs in a separate thread)
def jouer_note(note):
    if note in notes_dict:
        fichier_note = notes_dict[note]
        
        if os.path.isfile(fichier_note):
            # Load the WAV file in memory
            note_sound = AudioSegment.from_wav(fichier_note)
            
            # Play the note using pygame
            son = pygame.mixer.Sound(fichier_note)
            son.play()
            pygame.time.wait(int(note_sound.duration_seconds * 1000))  # Wait for the note to finish playing
        else:
            print(f"Le fichier {fichier_note} n'existe pas.")
    else:
        print("Note non reconnue.")

jouer_note('c3')

threshold = 0.01  # Threshold for detecting a spike (adjust based on your sensor)
spike_detected = False  # To track if a spike is detected
capture_duration = 0.15 # capture 1 second of data after spike
buffer_size = fs  # Buffer for one second of data
signal_buffer = np.zeros(buffer_size)  # Preallocate buffer for performance

# Function to plot data captured after a spike
def plot_data(data):
    t = np.linspace(0, dt, len(data))
    plt.plot(t, data)
    plt.xlabel('Time [s]')
    plt.ylabel('Amplitude')
    plt.title('Signal After Spike')
    plt.show()

# Callback function for real-time audio input
def audio_callback(indata, frames, time, status):
    global spike_detected, signal_buffer
    
    if status:
        print(status)
    
    # Flatten the input data
    audio_data = indata[:, 0]
    
    # Shift the buffer and add new data
    signal_buffer = np.roll(signal_buffer, -frames)
    signal_buffer[-frames:] = audio_data
    
    # Check for spike
    if not spike_detected and np.max(audio_data) > threshold:
        spike_detected = True
        print("Spike detected!")
    
        # Start a new thread to capture the next second of data
        capture_thread = threading.Thread(target=signal_analysis)
        capture_thread.start()

# Function to capture and plot the second after spike detection
def signal_analysis():
    global spike_detected
    
    time.sleep(capture_duration)  # Sleep for 1 second to gather post-spike data

    # Capture the buffer after the sleep duration
    post_spike_data = np.copy(signal_buffer)[int(fs-fs*capture_duration-800):]
    
##################################################################
# Data treatement
##################################################################

    data_max_amp = np.max(abs(post_spike_data))
    data_threshold = data_max_amp/10

    #Créer la fenêtre utilisée pour le signal
    for index,value in enumerate(post_spike_data):
        if value>=data_threshold:
            start_signal=index
            break
    cut_data = post_spike_data[start_signal:(start_signal+int(dt*fs))].flatten()

    # Plot the data
    #plot_data(cut_data)

    #Normalisation du signal
    norm_cut_data=cut_data/data_max_amp

    #Transformer la liste en array
    signal_array=np.array(norm_cut_data)

    #Produit scalaire (corrélation) entre les données de training et le signal test
    scalar_prod=np.dot(notes_matrix,signal_array)

    #Trouver l'indice de la valeur max du produit scalaire et trouver sa note correspondante
    index_max=np.argmax(scalar_prod)
    note_index=index_max//nb_recordings


    note = notes[note_index]
    if note:
        print(f"Playing note: {note}")
        # Start a new thread to play the note
        play_note_thread = threading.Thread(target=jouer_note, args=(note,))
        play_note_thread.start()
    
    # Reset spike detection to allow detecting future spikes
    spike_detected = False

# Start the audio stream
with sd.InputStream(callback=audio_callback, samplerate=fs, channels=1):
    print("Recording... (Press Ctrl+C to stop)")
    while True:
        time.sleep(0.001)  # Keep the main loop running

import threading
import time
import random
from collections import deque
import pygame
from pydub import AudioSegment
import os

# Initialize pygame mixer
pygame.mixer.init()

# Specify the path to ffmpeg
AudioSegment.ffmpeg = r'C:\ProgramData\chocolatey\bin\ffmpeg.exe'

# Dictionary to map signals to notes
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
    'a3': 'a3.wav',
    'a-3': 'a-3.wav',
    'b3': 'b3.wav'
}

# Function to play a note
def jouer_note(valeur):
    if valeur in notes_dict:
        fichier_note = notes_dict[valeur]
        if os.path.isfile(fichier_note):
            note = AudioSegment.from_wav(fichier_note)
            fichier_exporte = fichier_note  # Use original file
            son = pygame.mixer.Sound(fichier_exporte)
            son.play()
            pygame.time.wait(int(note.duration_seconds * 100))  # Wait for the note to finish playing
        else:
            print(f"Le fichier {fichier_note} n'existe pas.")
    else:
        print("Valeur non reconnue. Veuillez entrer une note valide.")

# Function to read sensor data and play music notes based on detected impulses
def read_sensor_data(buffer, pre_points, post_points, threshold):
    post_impulse_data_needed = 0  # Track post-impulse data collection

    while True:
        # Simulate sensor data (replace with actual sensor readings)
        signal = random.uniform(0, 1)  # Simulating sensor data
        buffer.append(signal)  # Store the signal in the rolling buffer

        # Check if we are capturing post-impulse data
        if post_impulse_data_needed > 0:
            post_impulse_data_needed -= 1
            if post_impulse_data_needed == 0:
                print(f"Captured signal: {list(buffer)}")
                captured_signal = list(buffer)  # Capture the full signal (pre and post)
                
                # Map the signal to a note and play it
                mapped_note = map_signal_to_note(captured_signal)
                if mapped_note:
                    jouer_note(mapped_note)
        
        # Detect an impulse
        elif signal > threshold:
            print(f"Impulse detected with signal: {signal}")
            post_impulse_data_needed = post_points  # Start capturing post-impulse data
            print("Capturing post-impulse data...")

        time.sleep(0.05)  # Simulate sensor read delay

# Map a captured signal to a specific note (this is a basic example, adjust as needed)
def map_signal_to_note(captured_signal):
    avg_signal = sum(captured_signal) / len(captured_signal)
    if avg_signal < 0.2:
        return 'c3'
    elif avg_signal < 0.4:
        return 'd3'
    elif avg_signal < 0.6:
        return 'e3'
    elif avg_signal < 0.8:
        return 'f3'
    else:
        return 'g3'

# Parameters for the rolling buffer
pre_points = 50  # Number of data points before the impulse
post_points = 50  # Number of data points after the impulse
threshold = 0.1  # Impulse detection threshold

# Create a circular buffer to hold the pre- and post-impulse data
buffer = deque(maxlen=pre_points + post_points)

# Start the thread that continuously reads sensor data
sensor_thread = threading.Thread(target=read_sensor_data, args=(buffer, pre_points, post_points, threshold))
sensor_thread.start()

# Main program continues (could handle other tasks)
while True:
    print("Main program running...")
    time.sleep(1)

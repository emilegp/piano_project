import threading
import time
import random
from collections import deque
import pygame
from pydub import AudioSegment
import os

# Specify the full path to ffmpeg
#AudioSegment.ffmpeg = r'C:\ProgramData\chocolatey\bin\ffmpeg.exe'

# Dictionary of notes and their corresponding WAV files
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

# Function to generate random signals
def generate_signal(buffer, threshold):
    while True:
        signal = random.uniform(0, 1)  # Generate a random number between 0 and 1
        buffer.append(signal)  # Add the signal to the buffer
        print(f"Generated signal: {signal:.3f}")
        time.sleep(0.1)  # Simulate some delay in signal generation
        print(buffer)

# Function to analyze the signal and trigger the note playing thread
def analyze_signal(buffer, threshold):
    while True:
        if any(s > threshold for s in buffer):
            captured_data = list(buffer)[-20:]  # Capture last 20 points
            print(captured_data)
            if captured_data:
                avg = sum(captured_data) / len(captured_data)
                print(f"Average of captured data: {avg:.3f}")
                
                # Map the average to a musical note based on value ranges
                note = map_value_to_note(avg)
                if note:
                    print(f"Playing note: {note}")
                    # Start a new thread to play the note
                    play_note_thread = threading.Thread(target=jouer_note, args=(note,))
                    play_note_thread.start()  # Start the music in a separate thread

            # Sleep briefly to avoid rapid re-triggering
            time.sleep(2)
        time.sleep(0.1)

# Function to map the average value to a musical note
def map_value_to_note(avg):
    if avg < 0.2:
        return 'c3'
    elif 0.2 <= avg < 0.3:
        return 'd3'
    elif 0.3 <= avg < 0.4:
        return 'e3'
    elif 0.4 <= avg < 0.5:
        return 'f3'
    elif 0.5 <= avg < 0.6:
        return 'g3'
    elif 0.6 <= avg < 0.7:
        return 'a3'
    elif 0.7 <= avg < 0.8:
        return 'b3'
    else:
        return None  # No note for values above 0.8

# Parameters
buffer_size = 50  # Buffer to store last N signals
threshold = 0.8   # Threshold to trigger data capture

# Shared circular buffer between threads
signal_buffer = deque(maxlen=buffer_size)

# Create threads
signal_thread = threading.Thread(target=generate_signal, args=(signal_buffer, threshold))
analyze_thread = threading.Thread(target=analyze_signal, args=(signal_buffer, threshold))

# Start the threads
signal_thread.start()
analyze_thread.start()

# Keep the main program running
signal_thread.join()
analyze_thread.join()


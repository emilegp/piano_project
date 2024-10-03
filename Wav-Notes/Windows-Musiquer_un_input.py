# Objectif: Faire une fonction qui prend en input une valeur et 
# sort de la musique


# Étapes :
# Installe pygame (si ce n'est pas déjà fait) avec la commande suivante :
# pip install pygame 
# Installe pydub (si ce n'est pas déjà fait) avec la commande suivante :
# pip install pydub 
# run

import pygame
from pydub import AudioSegment
import os

# Spécifie le chemin complet vers ffmpeg
AudioSegment.ffmpeg = r'C:\ProgramData\chocolatey\bin\ffmpeg.exe'

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

# Initialisation de pygame
pygame.mixer.init()

def jouer_note(valeur):
    if valeur in notes_dict:
        fichier_note = notes_dict[valeur]

        if os.path.isfile(fichier_note):
            # Charger le fichier WAV en mémoire
            note = AudioSegment.from_wav(fichier_note)
            
            # Exporter l'audio au format WAV en mémoire et le jouer avec pygame
            fichier_exporte = fichier_note  # Utiliser le fichier d'origine ici
            son = pygame.mixer.Sound(fichier_exporte)
            son.play()
            pygame.time.wait(int(note.duration_seconds * 150))  # Attendre la fin de la lecture
        elif os.path.isfile(f"\\Wav-Notes\\{notes_dict[valeur]}"):
            fichier_note = f"\\Wav-Notes\\{notes_dict[valeur]}"
            # Charger le fichier WAV en mémoire
            note = AudioSegment.from_wav(fichier_note)
            
            # Exporter l'audio au format WAV en mémoire et le jouer avec pygame
            fichier_exporte = fichier_note  # Utiliser le fichier d'origine ici
            son = pygame.mixer.Sound(fichier_exporte)
            son.play()
            pygame.time.wait(int(note.duration_seconds * 150))  # Attendre la fin de la lecture
        else:
            print(f"Le fichier {fichier_note} n'existe pas.")
    else:
        print("Valeur non reconnue. Veuillez entrer une note valide.")

#valeur = input("Entrez une note (c3, c-3, d3, d-3, e3, f3, f-3, g3, g-3, a3, a-3, b3) : ").lower()
#jouer_note(valeur)
#valeur2 = input("Entrez une 2e note (c3, c-3, d3, d-3, e3, f3, f-3, g3, g-3, a3, a-3, b3) : ").lower()
#jouer_note(valeur2)
#Jouer la gamme
for i in notes_dict:
    jouer_note(i)


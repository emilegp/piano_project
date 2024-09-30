# Objectif: Faire une fonction qui prend en input une valeur et 
# sort de la musique


#ChatGPT:
# Étapes :
# Installe pydub (si ce n'est pas déjà fait) avec la commande suivante :
# pip install pydub 
# Installe également ffmpeg ou libav pour permettre à pydub de lire des fichiers WAV. 
# Tu peux télécharger et installer ffmpeg ici: https://ffmpeg.org/download.html.
# Pour installer ffmpeg, installer chocolatey 
#@"%SystemRoot%\System32\WindowsPowerShell\v1.0\powershell.exe" -NoProfile -InputFormat None -ExecutionPolicy Bypass -Command "Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.SecurityProtocolType]::Tls12; Invoke-Expression ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))" && SET "PATH=%PATH%;%ALLUSERSPROFILE%\chocolatey\bin"
# Une fois chocolatey installé, installer ffmpeg 
# choco install ffmpeg
# Organise tes fichiers WAV dans un répertoire en nommant chaque fichier selon la note (par exemple : C.wav, D.wav, etc.).
# Crée la fonction en Python.

from pydub.playback import play
from pydub import AudioSegment
import os
print("Répertoire de travail actuel :", os.getcwd())

# Spécifie le chemin complet vers ffmpeg
AudioSegment.ffmpeg = r'C:\ProgramData\chocolatey\bin\ffmpeg.exe'

# Dictionnaire associant les valeurs aux fichiers audio des notes
notes_dict = {
    'c3': 'c3.wav',
    'd3': 'd3.wav',
    'e3': 'e3.wav',
    'f3': 'f3.wav',
    'g3': 'g3.wav',
    'a-3': 'a-3.wav',
    'b3': 'b3.wav'
}

def jouer_note(valeur):
    # Vérifier que la valeur est dans le dictionnaire
    if valeur in notes_dict:
        fichier_note = notes_dict[valeur]
        
        # Vérifier si le fichier existe avant de le charger
        if os.path.isfile(fichier_note):
            # Charger le fichier audio
            note = AudioSegment.from_wav(fichier_note)
            
            # Jouer le fichier audio
            play(note)
        else:
            print(f"Le fichier {fichier_note} n'existe pas.")
    else:
        print("Valeur non reconnue. Veuillez entrer une note valide.")

# Exemple d'utilisation
valeur = input("Entrez une note (C3, D3, E3, F3, G3, A3, B3) : ")
jouer_note(valeur)




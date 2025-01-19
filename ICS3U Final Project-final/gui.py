import PySimpleGUI as sg #makes the gui
import threading#used to run multiple things at a time
import pygame#the engine used to run the game
import subprocess#used to run the game
#please note ai and externel resourses were used to make this 


def play_music():
    pygame.mixer.init()
    pygame.mixer.music.load("sea.mp3")  # Load the audio file
    pygame.mixer.music.play(-1)

# creates the button and the text above it
layout = [
    [sg.Text("Arrgh ye scurvy pirate, welcome to All Aboard! use the left and right arrow keys to move ye ship, dodge the obsticles that appear")],
    [sg.Button("AYE AYE CAPTAIN")],
]


window = sg.Window("All Aboard!", layout)

# Start the music in a separate thread
music_thread = threading.Thread(target=play_music, daemon=True)
music_thread.start()


while True:
    event, values = window.read()

        
    if event in ("AYE AYE CAPTAIN", sg.WIN_CLOSED): #when the button is clicked it stop the music and 
        pygame.mixer.music.stop()  # Stops the music
       
        subprocess.run(["python", "game_ver6.py"]) #runs the actual game
        break

window.close()
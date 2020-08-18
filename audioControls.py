##This file is to simply hold the functions which run the subprocess for playing audio within the app
##Probably not neccessary, but was for me to learn about splitting into several files and using threads etc
##Plans to add while loops to prevent button being clicked again whilst audio is already playing
import subprocess
from subprocess import CREATE_NO_WINDOW

def play_beginning(command_play):
    subprocess.Popen(command_play, stderr=subprocess.DEVNULL, creationflags=CREATE_NO_WINDOW)

def play_end(command_end):
    subprocess.Popen(command_end, stderr=subprocess.DEVNULL, creationflags=CREATE_NO_WINDOW)

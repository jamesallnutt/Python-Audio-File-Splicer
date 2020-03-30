import tkinter as tk #Tkinter Module input as tk to save typing tkinter everytime
from tkinter import font
from tkinter import filedialog
from tkinter import *
from tkinter import ttk #Secondary Tkinter Module which includes Progress Bar
from threading import Thread #Module that allows Threading
from queue import Queue, Empty
from subprocess import Popen, PIPE, run #Module that allows running OS Processes
from functools import reduce
import os
import sys
import time
import subprocess

class Window:
    def __init__(self, main_window):
        self.main_window = main_window
        self.main_window.title("PyChop - Audio Editor")
        self.main_window.iconbitmap(r'gui_element_graphics/favicon.ico')
        self.main_window.maxsize(800,400)
        self.main_window.minsize(800,400)

        #Loading the below functions on boot of the App - buttons, frames etc.
        self.social_media()
        self.project_management()
        self.current_project()

    def social_media(self):
        self.social_frame = tk.Frame(self.main_window, bg='#625772', width=61, height=400)
        self.social_frame.grid(row=0, column=0)
        self.social_frame.grid_propagate(False)

        self.app_logo = tk.PhotoImage(file=r'gui_element_graphics/sidebar/audio_logo.png')
        app_logo = tk.Button(self.social_frame, image=self.app_logo, width=29, height=29)
        app_logo.config(bg='#625772', borderwidth=0, highlightthickness=0, bd=0, relief=FLAT)
        app_logo.grid(row=1, column=1, padx=13, pady=5)

        self.twitter_logo = tk.PhotoImage(file=r'gui_element_graphics/sidebar/twitter_logo.png')
        twitter_button = tk.Button(self.social_frame, image=self.twitter_logo, width=29, height=29)
        twitter_button.configure(bg='#625772', borderwidth=0, highlightthickness=0, bd=0, relief=FLAT)
        twitter_button.grid(row=2, column=1, padx=13, pady=(245,0))

        self.github_logo = tk.PhotoImage(file=r'gui_element_graphics/sidebar/github_logo.png')
        github_button = tk.Button(self.social_frame, image=self.github_logo, width=29, height=28)
        github_button.configure(bg='#625772', borderwidth=0, highlightthickness=0, bd=0, relief=FLAT)
        github_button.grid(row=3, column=1, padx=13, pady=(4,7))

        self.help_logo = tk.PhotoImage(file=r'gui_element_graphics/sidebar/help_logo.png')
        help_button = tk.Button(self.social_frame, image=self.help_logo, width=28, height=28)
        help_button.configure(bg='#625772', borderwidth=0, highlightthickness=0, bd=0, relief=FLAT)
        help_button.grid(row=4, column=1, padx=13)

    def project_management(self):
        self.save_management = tk.Frame(self.main_window, bg='#F6F6F6', width=226, height=400)
        self.save_management.grid(row=0, column=1)
        self.save_management.grid_propagate(False)

        header = tk.Label(self.save_management, text="Audio Projects", bg='#F6F6F6', fg='#69686D', font=('Helvetica', 14, 'bold'))
        header.grid(row=1, column=1, padx=(5,0), pady=(15,0))

        new_project = tk.Button(self.save_management, text="X")
        new_project.configure(bg='#F6F6F6', borderwidth=0, highlightthickness=0, bd=0, relief=FLAT)
        new_project.grid(row=1, column=2, padx=(80,0), pady=(15,0))

        search = tk.Entry(self.save_management)
        search.grid(row=2, column=1, columnspan=2, padx=(5,0), pady=(5), sticky=W)

        current_header = tk.Label(self.save_management, text="Current Project", bg='#F9A1BC', fg='#FFFFFF')
        current_header.grid(row=3, column=1, padx=(5,0), sticky=W)

        past_header = tk.Label(self.save_management, text="Past Projects", bg='#A9BCEE', fg='#FFFFFF')
        past_header.grid(row=5, column=1, padx=(5,0), sticky=W)

    def current_project(self):
        self.current_audio_project = tk.Frame(self.main_window, bg='#FFFFFF', height=400, width=452)
        self.current_audio_project.grid(row=0, column=2)
        self.current_audio_project.grid_propagate(False)

        current_header = tk.Label(self.current_audio_project, text="Current Project", bg='#F9A1BC', fg='#FFFFFF')
        current_header.grid(row=1, column=1, padx=(5,0), sticky=W, pady=(15,0))

        header = tk.Label(self.current_audio_project, text="Audio Editing Tools", bg='#FFFFFF', fg='#69686D', font=('Helvetica', 14, 'bold'))
        header.grid(row=2, column=1, padx=(5,0), sticky=W)

        browse_header = tk.Label(self.current_audio_project, text="Browse", bg='#FFFFFF', fg='#69686D', font=('Helvetica', 14, 'bold'))
        browse_header.grid(row=4, column=1, padx=(5,0), sticky=W)

        editing_header = tk.Label(self.current_audio_project, text="Export Options", bg='#FFFFFF', fg='#69686D', font=('Helvetica', 14, 'bold'))
        editing_header.grid(row=6, column=1, padx=(5,0), sticky=W)

if __name__ == "__main__":
    root = tk.Tk()
    my_window = Window(root)
    root.mainloop()
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


class Audio_Manager:
    def __init__(self, audio_window):
        self.audio_window = audio_window
        self.audio_window.title("PyChop - Audio Editor")
        self.audio_window.iconbitmap(r'gui_element_graphics/favicon.ico')
        self.audio_window.maxsize(800,400)
        self.audio_window.minsize(800,400)
        self.audio_window.configure(bg='#FFFFFF')


        #Loading the below functions on boot of the App - buttons, frames etc.
        self.social_media()
        self.project_management_headers()
        self.project_management_current()
        self.project_management_past()
        self.current_project_headers()
        self.current_project_tools()
        self.key_bindings()

    def social_media(self):
        self.social_frame = tk.Frame(self.audio_window, bg='#625772', width=61, height=400)
        self.social_frame.grid(row=0, column=0)
        self.social_frame.grid_propagate(False)

        self.app_logo = tk.PhotoImage(file=r'gui_element_graphics/sidebar/audio_logo.png')
        app_logo = tk.Button(self.social_frame, image=self.app_logo, width=30, height=30)
        app_logo.config(bg='#625772', borderwidth=0, highlightthickness=0, bd=0, relief=FLAT)
        app_logo.grid(row=1, column=1, padx=13, pady=5)

        self.twitter_logo = tk.PhotoImage(file=r'gui_element_graphics/sidebar/twitter_logo.png')
        twitter_button = tk.Button(self.social_frame, image=self.twitter_logo, width=31, height=31)
        twitter_button.configure(bg='#625772', borderwidth=0, highlightthickness=0, bd=0, relief=FLAT)
        twitter_button.grid(row=2, column=1, padx=13, pady=(245,0))

        self.github_logo = tk.PhotoImage(file=r'gui_element_graphics/sidebar/github_logo.png')
        github_button = tk.Button(self.social_frame, image=self.github_logo, width=31, height=31)
        github_button.configure(fg='#625772', borderwidth=0, highlightthickness=0, bd=0, relief=FLAT)
        github_button.grid(row=3, column=1, padx=13, pady=(4,7))

        self.help_logo = tk.PhotoImage(file=r'gui_element_graphics/sidebar/help_logo.png')
        help_button = tk.Button(self.social_frame, image=self.help_logo, width=31, height=31)
        help_button.configure(bg='#625772', borderwidth=0, highlightthickness=0, bd=0, relief=FLAT)
        help_button.grid(row=4, column=1, padx=13)

    def project_management_headers(self):
        self.save_management = tk.Frame(self.audio_window, bg='#F6F6F6', width=226, height=400)
        self.save_management.grid(row=0, column=1)
        self.save_management.grid_propagate(False)

        header = tk.Label(self.save_management, text="Audio Projects", bg='#F6F6F6', fg='#69686D', font=('Helvetica', 12, 'bold'))
        header.grid(row=1, column=1, padx=(5,0), pady=(15,0))

        new_project = tk.Button(self.save_management, text="X")
        new_project.configure(bg='#F6F6F6', borderwidth=0, highlightthickness=0, bd=0, relief=FLAT)
        new_project.grid(row=1, column=2, padx=(80,0), pady=(15,0))

        self.search = tk.Entry(self.save_management)
        self.search.grid(row=2, column=1, columnspan=2, padx=(5,0), pady=(5), sticky=W)
        self.search.insert(0, "Search")

        self.current_header_bg = tk.PhotoImage(file=r'gui_element_graphics/Current_Project.png')
        current_header = tk.Label(self.save_management, image=self.current_header_bg, text="Current Project", bg='#F6F6F6', fg='#FFFFFF', font=('Helvetica', 8, 'bold'), compound=CENTER)
        current_header.grid(row=3, column=1, padx=(5,0), sticky=W)

        past_header = tk.Label(self.save_management, text="Past Projects", bg='#A9BCEE', fg='#FFFFFF', font=('Helvetica', 8, 'bold'))
        past_header.grid(row=5, column=1, padx=(5,0), sticky=W)

    def project_management_current(self):

        self.save_current_project_info = tk.Frame(self.save_management, bg='#FFFFFF')
        self.save_current_project_info.grid(row=4, column=1, columnspan=2)
        self.save_current_project_info.grid_propagate(True)

        current_project_title = tk.Label(self.save_current_project_info, text="Filename:", fg='#69686D')
        current_project_title.grid(row=1, column=0, sticky=W)
        current_project_title_entry = tk.Label(self.save_current_project_info, text="Example Name")
        current_project_title_entry.grid(row=1, column=1, sticky=W)

        current_project_date = tk.Label(self.save_current_project_info, text='Date:', fg='#69686D')
        current_project_date.grid(row=2, column=0, sticky=W)
        current_project_recording_entry = tk.Label(self.save_current_project_info, text="Example Name")
        current_project_recording_entry.grid(row=2, column=1, sticky=W)

        current_project_recording = tk.Label(self.save_current_project_info, text='Start Time:', fg='#69686D')
        current_project_recording.grid(row=3, column=0, sticky=W)
        current_project_recording_entry = tk.Label(self.save_current_project_info, text="Example Name")
        current_project_recording_entry.grid(row=3, column=1, sticky=W)

    def project_management_past(self):
        self.past_project_info = tk.Frame(self.save_management, bg='#FFFFFF')
        self.past_project_info.grid(row=6, column=1, columnspan=2)
        self.past_project_info.grid_propagate(True)

        past_project_title_1 = tk.Label(self.past_project_info, text="Filename:", fg='#69686D')
        past_project_title_1.grid(row=1, column=0, sticky=W)
        past_project_title_1_entry = tk.Label(self.past_project_info, text="Example Name")
        past_project_title_1_entry.grid(row=1, column=1, sticky=W)

        past_project_date_1 = tk.Label(self.past_project_info, text='Date:', fg='#69686D')
        past_project_date_1.grid(row=2, column=0, sticky=W)
        past_project_date_1_entry = tk.Label(self.past_project_info, text="Example Name")
        past_project_date_1_entry.grid(row=2, column=1, sticky=W)

        past_project_recording_1 = tk.Label(self.past_project_info, text='Start Time:', fg='#69686D')
        past_project_recording_1.grid(row=3, column=0, sticky=W)
        past_project_recording_1_entry = tk.Label(self.past_project_info, text="Example Name")
        past_project_recording_1_entry.grid(row=3, column=1, sticky=W)

        past_project_title_2 = tk.Label(self.past_project_info, text="Filename:", fg='#69686D')
        past_project_title_2.grid(row=4, column=0, sticky=W)
        past_project_title_2_entry = tk.Label(self.past_project_info, text="Example Name")
        past_project_title_2_entry.grid(row=4, column=1, sticky=W)

        past_project_date_2 = tk.Label(self.past_project_info, text='Date:', fg='#69686D')
        past_project_date_2.grid(row=5, column=0, sticky=W)
        past_project_date_2_entry = tk.Label(self.past_project_info, text="Example Name")
        past_project_date_2_entry.grid(row=5, column=1, sticky=W)

        past_project_recording_2 = tk.Label(self.past_project_info, text='Start Time:', fg='#69686D')
        past_project_recording_2.grid(row=6, column=0, sticky=W)
        past_project_recording_2_entry = tk.Label(self.past_project_info, text="Example Name")
        past_project_recording_2_entry.grid(row=6, column=1, sticky=W)

        past_project_title_3 = tk.Label(self.past_project_info, text="Filename:", fg='#69686D')
        past_project_title_3.grid(row=7, column=0, sticky=W)
        past_project_title_3_entry = tk.Label(self.past_project_info, text="Example Name")
        past_project_title_3_entry.grid(row=7, column=1, sticky=W)

        past_project_date_3 = tk.Label(self.past_project_info, text='Date:', fg='#69686D')
        past_project_date_3.grid(row=8, column=0, sticky=W)
        past_project_date_3_entry = tk.Label(self.past_project_info, text="Example Name")
        past_project_date_3_entry.grid(row=8, column=1, sticky=W)

        past_project_recording_3 = tk.Label(self.past_project_info, text='Start Time:', fg='#69686D')
        past_project_recording_3.grid(row=9, column=0, sticky=W)
        past_project_recording_3_entry = tk.Label(self.past_project_info, text="Example Name")
        past_project_recording_3_entry.grid(row=9, column=1, sticky=W)

    def current_project_headers(self):
        self.current_audio_project = tk.Frame(self.audio_window, bg='#FFFFFF', height=400, width=452)
        self.current_audio_project.grid(row=0, column=2)
        self.current_audio_project.grid_propagate(False)


        self.current_header_backg = tk.PhotoImage(file=r'gui_element_graphics/Current_Project.png')
        current_header = tk.Label(self.current_audio_project, image=self.current_header_backg, compound=CENTER, text="Current Project", bg='#FFFFFF', fg='#FFFFFF', font=('Helvetica', 8, 'bold'))
        current_header.grid(row=1, column=1, padx=(5,0), sticky=W, pady=(15,0))

        browse = tk.Label(self.current_audio_project, text="Browse", bg='#FFFFFF', fg='#69686D', font=('Helvetica', 12, 'bold'))
        browse.grid(row=2, column=1, padx=(5,0), sticky=W)

        metadata = tk.Label(self.current_audio_project, text="Metadata (Optional)", bg='#FFFFFF', fg='#69686D', font=('Helvetica', 12, 'bold'))
        metadata.grid(row=4, column=1, padx=(5,0), sticky=W)

        editing_header = tk.Label(self.current_audio_project, text="Export Options", bg='#FFFFFF', fg='#69686D', font=('Helvetica', 12, 'bold'))
        editing_header.grid(row=6, column=1, padx=(5,0), sticky=W)

    def current_project_tools(self):
        current_file_path = tk.Label(self.current_audio_project, bg='#F6F6F6', text="Filepath here")
        current_file_path.grid(row=3, column=1, sticky=W, padx=(5,0))
        current_file_path.grid_propagate(True)
        current_file_button = tk.Button(self.current_audio_project)
        current_file_button.grid(row=3, column=2)

        metadata_file = tk.Label(self.current_audio_project, bg='#F6F6F6', text="Filepath here")
        metadata_file.grid(row=5, column=1, sticky=W, padx=(5,0))
        metadata_file_button = tk.Button(self.current_audio_project)
        metadata_file_button.grid(row=5, column=2)

        self.recording_date = tk.Entry(self.current_audio_project)
        self.recording_date.grid(row=7, column=1, padx=(5,0), sticky=W)
        self.recording_date.insert(0, "Recording Date")

        self.recording_start_time = tk.Entry(self.current_audio_project)
        self.recording_start_time.grid(row=8, column=1, padx=(5,0), sticky=W)
        self.recording_start_time.insert(0, "Recording Start Time")

        self.recording_start_bound = tk.Entry(self.current_audio_project)
        self.recording_start_bound.grid(row=9, column=1, padx=(5,0), sticky=W)
        self.recording_start_bound.insert(0, "Start Time Boundary")

        recording_start_bound_play = tk.Button(self.current_audio_project)
        recording_start_bound_play.grid(row=9, column=2)

        self.recording_end_bound = tk.Entry(self.current_audio_project)
        self.recording_end_bound.grid(row=10, column=1, padx=(5,0), sticky=W)
        self.recording_end_bound.insert(0, "End Time Boundary")

        recording_end_bound_play = tk.Button(self.current_audio_project)
        recording_end_bound_play.grid(row=10, column=2)

        self.recording_file_prefix = tk.Entry(self.current_audio_project)
        self.recording_file_prefix.grid(row=11, column=1, padx=(5,0), sticky=W)
        self.recording_file_prefix.insert(0, "Filename Prefix")

        progress = ttk.Progressbar(self.current_audio_project, orient = HORIZONTAL, length = 20)
        progress.grid(row=12, column=1, sticky='nswe', padx=(5,0), pady=10)
        progress.config(mode='determinate', maximum=99.99, value=0)

        export = tk.Button(self.current_audio_project)
        export.grid(row=12, column=2)

##Key Binds

    def key_bindings(self):
        self.search.bind("<FocusIn>", self.search_click)
        self.search.bind("<FocusOut>", self.search_out_focus)

        self.recording_date.bind("<FocusIn>", self.recording_date_click)
        self.recording_date.bind("<FocusOut>", self.recording_date_out_focus)

        self.recording_start_time.bind("<FocusIn>", self.recording_start_time_click)
        self.recording_start_time.bind("<FocusOut>", self.recording_start_time_out_focus)

        self.recording_start_bound.bind("<FocusIn>", self.recording_start_bound_click)
        self.recording_start_bound.bind("<FocusOut>", self.recording_start_bound_out_focus)

        self.recording_end_bound.bind("<FocusIn>", self.recording_end_bound_click)
        self.recording_end_bound.bind("<FocusOut>", self.recording_end_bound_out_focus)
        
        self.recording_file_prefix.bind("<FocusIn>", self.recording_file_prefix_click)
        self.recording_file_prefix.bind("<FocusOut>", self.recording_file_prefix_out_focus)

    def search_click(self, event):
        if self.search.get() == "Search":
            self.search.delete(0, "end")

    def search_out_focus(self, event):
        if self.search.get() == "":
            self.search.insert(0, "Search")

    def recording_date_click(self, event):
        if self.recording_date.get() == "Recording Date":
            self.recording_date.delete(0, "end")

    def recording_date_out_focus(self, event):
        if self.recording_date.get() == "":
            self.recording_date.insert(0, "Recording Date")

    def recording_start_time_click(self, event):
        if self.recording_start_time.get() == "Recording Start Time":
            self.recording_start_time.delete(0, "end")

    def recording_start_time_out_focus(self, event):
        if self.recording_start_time.get() == "":
            self.recording_start_time.insert(0, "Recording Start Time")

    def recording_start_bound_click(self, event):
        if self.recording_start_bound.get() == "Start Time Boundary":
            self.recording_start_bound.delete(0, "end")

    def recording_start_bound_out_focus(self, event):
        if self.recording_start_bound.get() == "":
            self.recording_start_bound.insert(0, "Start Time Boundary")

    def recording_end_bound_click(self, event):
        if self.recording_end_bound.get() == "End Time Boundary":
            self.recording_end_bound.delete(0, "end")

    def recording_end_bound_out_focus(self, event):
        if self.recording_end_bound.get() == "":
            self.recording_end_bound.insert(0, "End Time Boundary")

    def recording_file_prefix_click(self, event):
        if self.recording_file_prefix.get() == "Filename Prefix":
            self.recording_file_prefix.delete(0, "end")

    def recording_file_prefix_out_focus(self, event):
        if self.recording_file_prefix.get() == "":
            self.recording_file_prefix.insert(0, "Filename Prefix")


if __name__ == "__main__":
    root = tk.Tk()
    audio_window = Audio_Manager(root)

    root.mainloop()
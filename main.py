#This is a script made to cut audio from Case Catalyst for use on the Opus 2 Platform.
#It is written in python but compiled for support use in an EXE.
#It does require ffmpeg to be installed on machines before use.

import tkinter as tk
from tkinter import font
from tkinter import filedialog
from tkinter import *
from tkinter import ttk
import os
import sys
import time
import subprocess
from threading import Thread
from queue import Queue, Empty
from subprocess import Popen, PIPE, run
from functools import reduce
from test import du_stuff

class Window:
    def __init__(self, main_window):
        self.main_window = main_window
        self.customFont = font.Font(family="Lato", size=12)
        self.main_window.title("WAV Audio Chopping")
        self.main_window.configure(background='#F3F4F5')
        self.main_window.iconbitmap(r'gui_element_graphics\app_icon.ico')
        #self.main_window.maxsize(612,240)
        self.test_variable="This is a test"
        self.make_frames()
        self.make_buttons()
        self.make_entries()
        self.setup_keys()


#hide textbox blanks
    def setup_keys(self):
        self.start_time.bind("<Button-1>", self.start_time_click)
        self.start_time.bind("<FocusOut>", self.start_time_out_focus)

        self.end_time.bind("<Button-1>", self.end_time_click)
        self.end_time.bind("<FocusOut>", self.end_time_out_focus)

        self.sitting_date.bind("<Button-1>", self.date_click)
        self.sitting_date.bind("<FocusOut>", self.date_out_focus)

        self.timestamp_to_convert.bind("<Button-1>", self.timestamp_click)
        self.timestamp_to_convert.bind("<FocusOut>", self.timestamp_out_focus)

        self.casename.bind("<Button-1>", self.casename_click)
        self.casename.bind("<FocusOut>", self.casename_out_focus)

    def start_time_click(self, event):
        if self.start_time.get() == "HH:MM:SS":
            self.start_time.delete(0, "end")

    def start_time_out_focus(self, event):
        if self.start_time.get() == "":
            self.start_time.insert(0, 'HH:MM:SS')

    def end_time_click(self, event):
        if self.end_time.get() == "HH:MM:SS":
            self.end_time.delete(0, "end")

    def end_time_out_focus(self, event):
        if self.end_time.get() == "":
            self.end_time.insert(0, 'HH:MM:SS')

    def date_click(self, event):
        if self.sitting_date.get() == "DD-MM-YYYY":
            self.sitting_date.delete(0, "end")

    def date_out_focus(self, event):
        if self.sitting_date.get() == "":
            self.sitting_date.insert(0, 'DD-MM-YYYY')

    def timestamp_click(self, event):
        if self.timestamp_to_convert.get() == "HH:MM:SS":
            self.timestamp_to_convert.delete(0, "end")

    def timestamp_out_focus(self, event):
        if self.timestamp_to_convert.get() == "":
            self.timestamp_to_convert.insert(0, 'HH:MM:SS')

    def casename_click(self, event):
        if self.casename.get() == "Casename with Underscores":
            self.casename.delete(0, "end")

    def casename_out_focus(self, event):
        if self.casename.get() == "":
            self.casename.insert(0, "Casename with Underscores")

#frames layouts
    def make_frames(self):
        self.filedrop = tk.Frame(self.main_window)
        self.filedrop.grid(row=1, column=1, pady=10, padx=10)

        self.splice_input = tk.Frame(self.main_window)
        self.splice_input.grid(row=2, column=1, padx=5)

        self.date_input = tk.Frame(self.main_window)
        self.date_input.grid(row=3, column=1, padx=5)

        self.time_input = tk.Frame(self.main_window)
        self.time_input.grid(row=4, column=1, padx=5)

        self.buttons_location = tk.Frame(self.main_window)
        self.buttons_location.grid(row=5, column=1, pady=10)

        self.progress_bar_frame = tk.Frame(self.main_window)
        self.progress_bar_frame.grid(row=6, column=1, padx=10)


#entries layouts
    def make_entries(self):
        self.audio_entry = tk.Label(self.filedrop, background='#89929B', fg="White", highlightthickness=0, justify='center', relief='flat', width=50)
        self.audio_entry.grid(row=1, column=1, sticky='nswe')

        browsebutton = tk.Button(self.filedrop, text="Browse", command=self.click_browse)
        browsebutton.grid(row=1, column=2, sticky='nswe')

        start_label = tk.Label(self.splice_input, text="Start Time", bd=0, highlightthickness=0, relief='flat', bg='#F3F4F5', fg="#551A55", width=25)
        start_label.grid(row=1, column=1, sticky='nw')

        end_label = tk.Label(self.splice_input, text="End Time", bd=0, highlightthickness=0, relief='flat', bg='#F3F4F5', fg="#551A55", width=25)
        end_label.grid(row=2, column=1)

        date_label = tk.Label(self.date_input, text='Sitting Date', bd=0, highlightthickness=0, relief='flat', bg='#F3F4F5', fg="#551A55", width=25)
        date_label.grid(row=1, column=1)

        time_label = tk.Label(self.time_input, text='Timestamp', bd=0, highlightthickness=0, relief='flat', bg='#F3F4F5', fg="#551A55", width=25)
        time_label.grid(row=1, column=1)

        casename_label = tk.Label(self.time_input, text='Casename', bd=0, highlightthickness=0, relief='flat', bg='#F3F4F5', fg="#551A55", width=25)
        casename_label.grid(row=2, column=1)

        self.start_time = tk.Entry(self.splice_input, selectbackground='#0BB5C4', justify='left', font=('Lato'), relief="flat", width=35)
        self.start_time.grid(row=1, column=2)
        self.start_time.insert(0, 'HH:MM:SS')

        self.end_time = tk.Entry(self.splice_input, selectbackground='#0BB5C4', justify='left', font=('Lato'), relief="flat", width=35)
        self.end_time.grid(row=2, column=2)
        self.end_time.insert(0, 'HH:MM:SS')

        self.sitting_date = tk.Entry(self.date_input, selectbackground='#0BB5C4', justify='left', font=('Lato'), relief="flat", width=35)
        self.sitting_date.grid(row=1, column=2)
        self.sitting_date.insert(0, 'DD-MM-YYYY')

        self.timestamp_to_convert = tk.Entry(self.time_input, selectbackground='#0BB5C4', justify='left', font=('Lato'), relief="flat", width=35)
        self.timestamp_to_convert.grid(row=1, column=2)
        self.timestamp_to_convert.insert(0, 'HH:MM:SS')

        self.casename = tk.Entry(self.time_input, selectbackground='#0BB5C4', justify='left', font=('Lato'), relief="flat", width=35)
        self.casename.grid(row=2, column=2)
        self.casename.insert(0, 'Casename with Underscores')

#write layouts

    def progress_bar(self):
        progress_bar = ttk.ProgressBar(self.progress_bar_frame, mode='determinate', orient=HORIZONTAL, length=100)
        progressBar.progress_bar_thread()
        progress_bar.grid(row=1, column=0, sticky='nsew')
        progress_bar.start()

#buttons layout
    def make_buttons(self):
        save_button = tk.Button(self.buttons_location, text='Save Location', command=self.click_save_location, bg="#CCCCCC", relief="flat", width=25)
        save_button.grid(row=1, column=0, sticky='nsew')

        save_button = tk.Button(self.buttons_location, text='Chop and Convert', command=self.click_save, bg="#CCCCCC", relief="flat", width=25)
        save_button.grid(row=1, column=1, sticky='nsew')

        reset_button = tk.Button(self.buttons_location, text='Reset Timecodes', command=self.click_reset, bg="#CCCCCC", relief="flat", width=25)
        reset_button.grid(row=1, column=2, sticky='nsew')

        reset_all_button = tk.Button(self.buttons_location, text='Reset All', command=self.click_reset_all, bg="#CCCCCC", relief="flat", width=25)
        reset_all_button.grid(row=1, column=3, sticky='nsew')

#Reset Commands:
    def click_reset(self, *event):
        ttcvar = "HH:MM:SS"
        self.timestamp_to_convert.delete(0, 'end')
        self.timestamp_to_convert.insert(0, 'HH:MM:SS')
        etvar = "HH:MM:SS"
        self.end_time.delete(0, 'end')
        self.end_time.insert(0, 'HH:MM:SS')
        stvar = "HH:MM:SS"
        self.start_time.delete(0, 'end')
        self.start_time.insert(0, 'HH:MM:SS')
        progress.config(value=0)

    def click_reset_all(self, *event):
        ttcvar = "HH:MM:SS"
        self.timestamp_to_convert.delete(0, 'end')
        self.timestamp_to_convert.insert(0, 'HH:MM:SS')
        etvar = "HH:MM:SS"
        self.end_time.delete(0, 'end')
        self.end_time.insert(0, 'HH:MM:SS')
        stvar = "HH:MM:SS"
        self.start_time.delete(0, 'end')
        self.start_time.insert(0, 'HH:MM:SS')
        sdvar = "DD-MM-YYYY"
        self.sitting_date.delete(0, 'end')
        self.sitting_date.insert(0, 'DD-MM-YYYY')
        casename = "Casename with Underscores"
        self.casename.delete(0, 'end')
        self.casename.insert(0,'Casename with Underscores')
        self.audio_entry.configure(text='Load New File')
        progress.config(value=0)

#Grab Original File:
    def click_browse(self, *event):
        self.filename = filedialog.askopenfilename(title = "Select WAV/WMA/MPEG/MP4 file",filetypes = (("WAV Files","*.wav"),("WMA files","*.wma"),("MPEG files","*.mpeg"),("MP4 files","*.mp4"),("all files","*.*")))
        self.audio_entry.configure(text=self.filename)


    def click_save_location(self, *event):
        self.savelocation = filedialog.askdirectory(title = "Save Location")

    def click_save(self, *event):
        global progress
    ###Splitting out User Inputs of Timestamps:
        sttvar = self.start_time.get()
        etvar = self.end_time.get()
        sdvar = self.sitting_date.get()
        ttcvar = self.timestamp_to_convert.get()
        casename =  self.casename.get()

        start_hour, start_minute, start_second = sttvar.split(":")
        end_hour, end_minute, end_second = etvar.split(":")
        sitting_day, sitting_month, sitting_year = sdvar.split("-")
        epoch_time_hour, epoch_time_minute, epoch_time_second = ttcvar.split(":")
    ###NEW FILENAME
        date_time = sdvar + " " + ttcvar
        pattern = "%d-%m-%Y %H:%M:%S"
        epoch_time = int(time.mktime(time.strptime(date_time, pattern)))
        converted_time = hex(epoch_time)
        new_filename = self.savelocation + "/" + str(casename) + "_" + str(sitting_year) + str(sitting_month) + str(sitting_day) + "-" + str(epoch_time_hour) + str(epoch_time_minute) + "_" + str(converted_time) + ".wma"

    ###COMMAND TO RUN
        command = ["C:\\Program Files\\ffmpeg\\bin\\ffmpeg.exe", "-i", self.filename, "-ss", sttvar, "-to", etvar, "-async", "1", "-strict", "-2", "-ar", "44100", "-ab", "56k", "-ac", "1", "-y", new_filename]
        print(" ".join(command))
        self.end_time_calc = int(end_hour)*3600 + int(end_minute)*60 + int(end_second)
        self.start_time_calc = int(start_hour)*3600 + int(start_minute)*60 + int(start_second)
        target_file_duration = float(self.end_time_calc) - float(self.start_time_calc)

        def fun(percentage):
            # pass
            print(percentage * 100)
        Thread(target=lambda: du_stuff(command, target_file_duration, lambda x: progress.config(value=x*100))).start()


if __name__ == "__main__":
    root = tk.Tk()
    sdvar = " "
    ttcvar = " "
    etvar = " "
    sttvar = " "
    casename = " "
    epoch_time = 0
    converted_time = 0
    canvas = tk.Canvas(root, width=275, height=65, bd=0, highlightthickness=0, background='#F3F4F5')
    my_window = Window(root)
    progress = ttk.Progressbar(root, orient = HORIZONTAL, length = 20)
    progress.grid(row=7, column=1, sticky='nswe', padx=10, pady=10)
    progress.config(mode='determinate', maximum=99.99, value=0)
    root.mainloop()

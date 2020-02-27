#Within this file the GUI is built using the Tkinter Module. 
#In terms of structure, it isn't the clearest - but all falls within the class "Window"
#Some data is pulled from other files - such as the audio playback controls, 
#as well as the progress bar loading, this is done to allow Threading so the GUI doesn't lock up. 
#Any ideas on tidying this up a bit are very much welcomed. 

#Importing Modules
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

#Importing from other files in project
from progress_bar import du_stuff #du_stuff is the name of our load bar progress percentage on GUI
from audio_controls import play_beginning, play_end #these are the subprocess calls for ffplay to run playback

class Window:

###INITIALISE APP###

#This Function initialises the app plus any preferences set.
    def __init__(self, main_window):
        #Loading the Main window with set preferences, such as Font, App Icon and Title
        self.main_window = main_window
        self.main_window.title("PyChop - Audio Editor") #App Title - In OS System Bar
        #self.main_window.configure(background='#625772') #App Background Colour
        self.main_window.iconbitmap(r'gui_element_graphics/favicon.ico') #App Favicon

        #Loading the below functions on boot of the App - buttons, frames etc.
        self.make_frames()
        self.make_buttons()
        self.make_entries()
        self.setup_keys()
        self.audio_player_visuals()

####VISUALS###

#This Section is all about Frames. Frames are a vital part of Tkinter, they dictate the boundary area of labels, buttons etc for display purposes.

    def make_frames(self):
        self.filedrop = tk.Frame(self.main_window) #Browse for File Frame
        self.filedrop.grid(row=1, column=1, pady=10, padx=10)

        self.splice_input = tk.Frame(self.main_window) #Timestamp Entry and Label Frame
        self.splice_input.grid(row=3, column=1, padx=5)

        self.date_input = tk.Frame(self.main_window) #Date Entry and Label Frame
        self.date_input.grid(row=4, column=1, padx=5)

        self.casename_input = tk.Frame(self.main_window) #CaseName Entry and Label Frame
        self.casename_input.grid(row=5, column=1, padx=5)

        self.buttons_location = tk.Frame(self.main_window) #User Buttons Frame
        self.buttons_location.grid(row=6, column=1, pady=10)

        self.progress_bar_frame = tk.Frame(self.main_window) #Progress Bar Frame
        self.progress_bar_frame.grid(row=7, column=1, padx=10)

#This Section is about Entries. I.e. Where the User Types information such as Timestamps.

    def make_entries(self):
        
        self.audio_entry = tk.Label(self.filedrop, background='#89929B', fg="White", highlightthickness=0, justify='center', relief='flat', width=50) #Filepath Field - Shows Selected File or Default "Load File" text 
        self.audio_entry.grid(row=1, column=1, sticky='nswe')

        browsebutton = tk.Button(self.filedrop, text="Browse", command=self.click_browse) #Browse to grab file 
        browsebutton.grid(row=1, column=2, sticky='nswe')

        start_time_label = tk.Label(self.splice_input, text="Start Time", bd=0, highlightthickness=0, relief='flat', bg='#F3F4F5', fg="#551A55", width=25) #This section as the name suggests is just Labels
        start_time_label.grid(row=1, column=1, sticky='nw')

        start_segment_label = tk.Label(self.splice_input, text="Beginning of Segment", bd=0, highlightthickness=0, relief='flat', bg='#F3F4F5', fg="#551A55", width=25)
        start_segment_label.grid(row=2, column=1)

        end_label = tk.Label(self.splice_input, text="End of Segment", bd=0, highlightthickness=0, relief='flat', bg='#F3F4F5', fg="#551A55", width=25)
        end_label.grid(row=3, column=1)

        date_label = tk.Label(self.date_input, text='Sitting Date', bd=0, highlightthickness=0, relief='flat', bg='#F3F4F5', fg="#551A55", width=25)
        date_label.grid(row=1, column=1)

        casename_label = tk.Label(self.casename_input, text='Casename', bd=0, highlightthickness=0, relief='flat', bg='#F3F4F5', fg="#551A55", width=25)
        casename_label.grid(row=2, column=1)

        self.start_time = tk.Entry(self.splice_input, selectbackground='#0BB5C4', justify='left', font=('Lato'), relief="flat", width=35) #From here to the end of the function - this is all entry fields being created
        self.start_time.grid(row=1, column=2)
        self.start_time.insert(0, 'HH:MM:SS')

        self.start_segment_time = tk.Entry(self.splice_input, selectbackground='#0BB5C4', justify='left', font=('Lato'), relief="flat", width=35)
        self.start_segment_time.grid(row=2, column=2)
        self.start_segment_time.insert(0, 'HH:MM:SS')

        self.end_time = tk.Entry(self.splice_input, selectbackground='#0BB5C4', justify='left', font=('Lato'), relief="flat", width=35)
        self.end_time.grid(row=3, column=2)
        self.end_time.insert(0, 'HH:MM:SS')

        self.sitting_date = tk.Entry(self.date_input, selectbackground='#0BB5C4', justify='left', font=('Lato'), relief="flat", width=35)
        self.sitting_date.grid(row=1, column=2)
        self.sitting_date.insert(0, 'DD-MM-YYYY')

        self.casename = tk.Entry(self.casename_input, selectbackground='#0BB5C4', justify='left', font=('Lato'), relief="flat", width=35)
        self.casename.grid(row=2, column=2)
        self.casename.insert(0, 'Casename with Underscores')

#This Section is about building Buttons. I.E. What Users Click to Commit Actions
    def make_buttons(self):

        save_loc_button = tk.Button(self.buttons_location, text='Save Location', command=self.click_save_location, bg="#CCCCCC", relief="flat", width=25) #Wont explain these, text parameter explains their usage
        save_loc_button.grid(row=1, column=0, sticky='nsew')

        save_button = tk.Button(self.buttons_location, text='Chop and Convert', command=self.click_save, bg="#CCCCCC", relief="flat", width=25)
        save_button.grid(row=1, column=1, sticky='nsew')

        reset_button = tk.Button(self.buttons_location, text='Reset Timecodes', command=self.click_reset, bg="#CCCCCC", relief="flat", width=25)
        reset_button.grid(row=1, column=2, sticky='nsew')

        reset_all_button = tk.Button(self.buttons_location, text='Reset All', command=self.click_reset_all, bg="#CCCCCC", relief="flat", width=25)
        reset_all_button.grid(row=1, column=3, sticky='nsew')

#This Section builds the buttons for the Audio Playback of the sections inputted by users.
    def audio_player_visuals(self):

        self.play_icon = PhotoImage(file = r"gui_element_graphics/play.png") #Grabbing Free to Use Play Icon
        self.play_icon = self.play_icon.subsample(40,40) #Downscaling icon to fit on Button

        audio_play_start = tk.Button(self.splice_input, image=self.play_icon, width=20, command=self.click_play_start) #Button to play 10 seconds of audio from Start Timecode
        audio_play_start.grid(row=2, column=1, sticky=E)

        audio_play_end_minus_ten = tk.Button(self.splice_input, image=self.play_icon, width=20, command=self.click_play_end) #Button to play 10 seconds of audio before End TimeCode
        audio_play_end_minus_ten.grid(row=3, column=1, sticky=E)

###KEYBINDINGS###

#This Section Covers all keybindings within the platform - i.e. when the user clicks into an Entry Field

    def setup_keys(self): #Adding Keybinging to Entry Fields
        self.start_time.bind("<Button-1>", self.start_time_click) #Same for all below, click into box action *click
        self.start_time.bind("<FocusOut>", self.start_time_out_focus) #Same for all below, click into box action *focus

        self.start_segment_time.bind("<Button-1>", self.start_segment_click)
        self.start_segment_time.bind("<FocusOut>", self.start_segment_out_focus)

        self.end_time.bind("<Button-1>", self.end_time_click)
        self.end_time.bind("<FocusOut>", self.end_time_out_focus)

        self.sitting_date.bind("<Button-1>", self.date_click)
        self.sitting_date.bind("<FocusOut>", self.date_out_focus)

        self.casename.bind("<Button-1>", self.casename_click)
        self.casename.bind("<FocusOut>", self.casename_out_focus)

#This Section ties into the keybindings, this time, the Visual effects, e.g. adding in HH:MM:SS if the user leaves the Entry field blank but clicks elsewhere

    def start_time_click(self, event): #Same for below *click means, when clicking in box, if it is HH:MM:SS - delete all content, otherwise leave as is
        if self.start_time.get() == "HH:MM:SS":
            self.start_time.delete(0, "end")

    def start_time_out_focus(self, event): #Same for below *out focus means, when clicking out of box, if empty insert HH:MM:SS
        if self.start_time.get() == "":
            self.start_time.insert(0, 'HH:MM:SS')
    
    def start_segment_click(self, event):
        if self.start_segment_time.get() == "HH:MM:SS":
            self.start_segment_time.delete(0, "end")

    def start_segment_out_focus(self, event):
        if self.start_segment_time.get() == "":
            self.start_segment_time.insert(0, 'HH:MM:SS')

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

    def casename_click(self, event):
        if self.casename.get() == "Casename with Underscores":
            self.casename.delete(0, "end")

    def casename_out_focus(self, event):
        if self.casename.get() == "":
            self.casename.insert(0, "Casename with Underscores")

###ACTIONS###

#This Section covers the commands the Buttons action. I.E. The behind the scenes of what clicking the button does.

    def click_reset(self, *event): #Resetting just the Timestamps for Beginning and End of Segment, Plus Progress Bar
        etvar = "HH:MM:SS" #Clearing any data potentially stored in variable
        self.end_time.delete(0, 'end') #Same commands as keybindings effectively
        self.end_time.insert(0, 'HH:MM:SS')
        stsgvar = "HH:MM:SS"
        self.start_segment_time.delete(0, 'end')
        self.start_segment_time.insert(0, 'HH:MM:SS')
        progress.config(value=0)

    def click_reset_all(self, *event): #Same as above, but this resets all variables, progress bar, chosen file etc.
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
        stsgvar = "HH:MM:SS"
        self.start_segment_time.delete(0, 'end')
        self.start_segment_time.insert(0, 'HH:MM:SS')
        progress.config(value=0)

    def click_browse(self, *event): #Location file to load for segmenting
        global filename #Making this global as I use it later in click_play_start/end
        filename = filedialog.askopenfilename(title = "Select WAV/WMA/MPEG/MP4 file",filetypes = (("WAV Files","*.wav"),("WMA files","*.wma"),("MPEG files","*.mpeg"),("MP4 files","*.mp4"),("all files","*.*"))) #Using filedialogue module, dictating which file types can be inputted - can change this to your preference if you want to limit
        self.audio_entry.configure(text=filename) #updating audio entry field to display filepath - might change this just to show filename

    def click_save_location(self, *event): #As simple as, where does the user want the end file to save
        self.savelocation = filedialog.askdirectory(title = "Save Location")

    def click_save(self, *event): #This is a big function - will explain each step.
        global progress #Bringing in global variable of progress, which is for the loading bar

        sttvar = self.start_time.get() #Here we are updating variables to have the contents of the Entry Fields as populated by the End User
        stsgvar = self.start_segment_time.get()
        etvar = self.end_time.get()
        sdvar = self.sitting_date.get()
        casename =  self.casename.get()

        start_hour, start_minute, start_second = sttvar.split(":") #Using Split I am breaking up the variables which are in HH:MM:SS and dd-mm-yyyy into subvariables, could proably do this in one step, but would take more work to undo.
        start_seg_hour, start_seg_minute, start_seg_second = stsgvar.split(":")
        end_hour, end_minute, end_second = etvar.split(":")
        sitting_day, sitting_month, sitting_year = sdvar.split("-")
        epoch_time_hour, epoch_time_minute, epoch_time_second = stsgvar.split(":")

            #This section is only really for the purposes of my project where the audio is linked to a transcript#
            #You can if you like ignore most of this, and just do "new_filename = "whatever you wanna have""
        date_time = sdvar + " " + stsgvar #building for filename, which requires sitting date + start of section time 
        pattern = "%d-%m-%Y %H:%M:%S" #defining the pattern to understand date_time
        epoch_time = int(time.mktime(time.strptime(date_time, pattern))) #getting epoch time - using pattern + date_time and mktime from time module
        converted_time = hex(epoch_time) #converting epoch time to hex value
        new_filename = self.savelocation + "/" + str(casename) + "_" + str(sitting_year) + str(sitting_month) + str(sitting_day) + "-" + str(epoch_time_hour) + str(epoch_time_minute) + "_" + str(converted_time) + ".wma" #building new filename
    
            #This section does a bit of maths. So most audio files start at 00:00:00 - however in the context of my project, they match with timecodes in clock elapsed time##
            ##For example, rather than 01:30:23 being 1hr, 30min, 23secs into the file, this would mean 01:30am##
            ##If you want to skip this, just change the variables listed below##
        self.start_time_calc = int(start_hour)*3600 + int(start_minute)*60 + int(start_second)
        self.start_segment_time_calc = int(start_seg_hour)*3600 + int(start_seg_minute)*60 + int(start_seg_second)
        self.end_time_calc = int(end_hour)*3600 + int(end_minute)*60 + int(end_second)

            ##After above maths, below is result - here I am telling FFMPEG - if the user says the recording started at 09:00am##
            ##and the first bit they want is at 10:30am - chop the audio at 01:30:00 time in, as this is effectively the same##
        actual_start_segment = float(self.start_segment_time_calc) - float(self.start_time_calc)
        actual_end_segment = float(self.end_time_calc) - float(self.start_time_calc)
        target_file_duration = float(actual_end_segment) - float(actual_start_segment)
    
            ##First Threading here - bringing in function du_stuff from progress_bar.py##
            ##Creating Command String to add to Thread - saying, use ffmpeg, file is variable filename, start time is -ss and end time is -to, plus a variety of parameters for quality before renaming as new_filename##
        command = ["/Volumes/Secondary Disk/Git Projects/Python-Audio-Choppin/ffmpeg/bin/ffmpeg", "-i", filename, "-ss", str(actual_start_segment), "-to", str(actual_end_segment), "-async", "1", "-strict", "-2", "-ar", "44100", "-ab", "56k", "-ac", "1", "-y", new_filename]
        Thread(target=lambda: du_stuff(command, target_file_duration, lambda x: progress.config(value=x*100))).start()

    def click_play_start(self, *event): ##Playing Audio for Start of Section for 10 seconds
            ##See Click Save function for breakdown on below, does the same maths as within that function - could probably do some sort of global one of these to save it being reproduced, feel free to create branch!
        sttvar = self.start_time.get()
        stsgvar = self.start_segment_time.get()

        start_hour, start_minute, start_second = sttvar.split(":")
        start_seg_hour, start_seg_minute, start_seg_second = stsgvar.split(":")

        self.start_time_calc = int(start_hour)*3600 + int(start_minute)*60 + int(start_second)
        self.start_segment_time_calc = int(start_seg_hour)*3600 + int(start_seg_minute)*60 + int(start_seg_second)

        actual_start_segment = float(self.start_segment_time_calc) - float(self.start_time_calc)

            ##Added -nodisp and -autoexit to ffplay command to hide CMD window and close the process in background when clip is done##
        command_play = ["/Volumes/Secondary Disk/Git Projects/Python-Audio-Choppin/ffmpeg/bin/ffplay", filename, "-ss", str(actual_start_segment), "-t", "10", "-nodisp", "-autoexit"] #Slightly different as using ffplay. But -t 10 means end at 10 seconds after start. Can change time to however many seconds.
        Thread(target=lambda: play_beginning(command_play)).start()

    def click_play_end(self, *event): ##Same as click_play_start, but for end boundary of clip, plays 10 seconds before user defined end
        sttvar = self.start_time.get()
        start_hour, start_minute, start_second = sttvar.split(":")
        self.start_time_calc = int(start_hour)*3600 + int(start_minute)*60 + int(start_second)

        etvar = self.end_time.get()
        end_hour, end_minute, end_second = etvar.split(":")
        self.end_time_calc = int(end_hour)*3600 + int(end_minute)*60 + int(end_second)

        end_segment = float(self.end_time_calc) - float(self.start_time_calc)
        actual_end_segment = float(end_segment) - 10 #taking away 10 seconds from end segment
        
        command_play = ["/Volumes/Secondary Disk/Git Projects/Python-Audio-Choppin/ffmpeg/bin/ffplay", filename, "-ss", str(actual_end_segment), "-t", "10", "-nodisp", "-autoexit"]
        Thread(target=lambda: play_end(command_play)).start()

if __name__ == "__main__":
    root = tk.Tk()
    my_window = Window(root)

        #Ensuring String Variables set to empty to start
    filename = " "
    sdvar = " "
    ttcvar = " "
    etvar = " "
    sttvar = " "
    stsgvar = " "
    casename = " "

        #Ensuring Integer Variables set to 0 to start
    epoch_time = 0
    converted_time = 0

        #Progress Bar Loading aways when running
    progress = ttk.Progressbar(root, orient = HORIZONTAL, length = 20)
    progress.grid(row=7, column=1, sticky='nswe', padx=10, pady=10)
    progress.config(mode='determinate', maximum=99.99, value=0)

    root.mainloop()


    #canvas = tk.Canvas(root, width=275, height=65, bd=0, highlightthickness=0, background='#F3F4F5')
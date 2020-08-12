import tkinter as tk #Tkinter Module input as tk to save typing tkinter everytime
from tkinter import font
from tkinter import filedialog
from tkinter import *
from tkinter import ttk #Secondary Tkinter Module which includes Progress Bar
from threading import Thread #Module that allows Threading
from ttkthemes import ThemedTk
from queue import Queue, Empty
from subprocess import Popen, PIPE, run #Module that allows running OS Processes
from functools import reduce
import ffmpy
from ffmpy import FFmpeg
import tkcalendar as tkc
import os
import pickle
import sys
import time
import datetime
import subprocess
import webbrowser
import json

from progressBar import progress_bar_percent #progress_bar_percent is the name of our load bar progress percentage on GUI
from audioControls import play_beginning, play_end #these are the subprocess calls for ffplay to run playback

class Splash(tk.Toplevel):
    def __init__(self, parent):
        tk.Toplevel.__init__(self, parent)
        self.overrideredirect(1)
        self.configure(bg='#625772')
        self.splash_image = tk.PhotoImage(master=self, file=resource_path("gui_element_graphics\\splash_screen\\splashScreen.png"))
        self.splash_canvas = Canvas(master=self, width=300, height=400, bd=0, bg='#625772', highlightthickness=0, relief='ridge')
        self.splash_canvas.grid(row=0, column=0, sticky='nswe')
        self.splash_canvas.grid_propagate(True)
        self.splash_canvas.create_image(0, 0, anchor=NW, image=self.splash_image)
        self.center_splash_screen()
        self.update()

    def center_splash_screen(self):
        w = 300
        h = 400
        ws = root.winfo_screenwidth() # width of the screen
        hs = root.winfo_screenheight() # height of the screen
        x = (ws/2) - (w/2)
        y = (hs/2) - (h/2)
        self.geometry('%dx%d+%d+%d' % (w, h, x, y))

class Production_Tools(tk.Tk):
    def __init__(self, main_window):
        tk.Tk.__init__(self)
        self.withdraw()
        main_window.withdraw()
        splash = Splash(self)
        self.main_window = main_window
        self.main_window.title("tool.box")
        self.main_window.iconbitmap(resource_path("app_icon.ico"))
        self.main_window.maxsize(690,400)
        self.main_window.minsize(690,400)
        self.main_window.configure(bg='#625772')
        self.main_window.update()

        self.tab_management()
        #self.file_page()
        self.audio_page()
        self.sidebar()
        self.main_window.update()

        self.tab_creation = ttk.Notebook(self.tab_frame)
        self.tab_creation.add(self.audio_tool_page)
        #self.tab_creation.add(self.file_tool_page)
        self.tab_creation.grid(row=0,column=0)
        self.main_window.update()

        self.project_management_headers()
        self.project_management()
        self.current_project_headers()
        self.current_project_tools()
        #self.files_job_management()
        #self.project_file_management()
        #self.current_project_file_headers()
        self.key_bindings()
        self.load_previous_projects_on_launch()
        #self.transcriptProductionConfig()
        self.main_window.update()
        
        self.selected_tab = tk.PhotoImage(file=resource_path("gui_element_graphics\\sidebar\\selected_tab.png"))
        self.selected_tab_icon = tk.Label(self.social_frame, image=self.selected_tab, width=6, height=40)
        self.selected_tab_icon.config(bg='#625772', borderwidth=0, highlightthickness=0, bd=0, relief=FLAT)
        self.selected_tab_icon.grid(row=0, column=0, sticky=SW)
        self.main_window.update()

        time.sleep(6)
        tk.Tk.destroy(self)
        self.main_window.deiconify()
        
    def tab_management(self):
        self.tab_frame = tk.Frame(self.main_window, bg='#625772')
        self.tab_frame.grid(row=0,column=0, padx=(35,0))
        self.tab_frame.grid_propagate(True)

    def tab_nav_1(self):
        self.tab_creation.select(self.audio_tool_page)
        self.selected_tab_icon.grid(row=0, column=0, sticky=SW)

    def tab_nav_2(self):
        self.tab_creation.select(self.file_tool_page)
        self.selected_tab_icon.grid(row=1, column=0, sticky=SW)

    def audio_page(self):
        self.audio_tool_page = tk.Frame()
        self.audio_tool_page.grid(row=0, column=0)
        self.audio_tool_page.grid_propagate(True)
    
    def file_page(self):
        self.file_tool_page = tk.Frame()
        self.file_tool_page.grid(row=0, column=0)

    def sidebar(self):
        self.social_frame = tk.Frame(self.main_window, bg='#625772', width=50, height=400)
        self.social_frame.grid(row=0, column=0, sticky=NW)
        self.social_frame.grid_propagate(False)

        self.audio_logo = tk.PhotoImage(file=resource_path("gui_element_graphics\\sidebar\\icon_audio.png"))
        audio_logo = tk.Button(self.social_frame, image=self.audio_logo, width=30, height=40)
        audio_logo.config(bg='#625772', borderwidth=0, highlightthickness=0, bd=0, relief=FLAT, command=self.tab_nav_1)
        audio_logo.grid(row=0, column=1, padx=10, pady=5, sticky=W)
        
        self.file_logo = tk.PhotoImage(file=resource_path("gui_element_graphics\\sidebar\\icon_file.png"))
        file_logo = tk.Button(self.social_frame, image=self.file_logo, width=30, height=40)
        file_logo.config(bg='#625772', borderwidth=0, highlightthickness=0, bd=0, relief=FLAT, command=self.tab_nav_2)
        file_logo.grid(row=1, column=1, padx=10, pady=5, sticky=W)

        self.help_logo = tk.PhotoImage(file=resource_path('gui_element_graphics\\sidebar\\help_logo.png'))
        help_button = tk.Button(self.social_frame, image=self.help_logo, width=31, height=31)
        help_button.configure(bg='#625772', borderwidth=0, highlightthickness=0, bd=0, relief=FLAT, command=self.open_credits)
        help_button.grid(row=4, column=1, padx=10, pady=(260,0), sticky=SW)

    def open_credits(self):
            credits_window = Toplevel(root)
            credits_window.overrideredirect(1)

            w = 300
            h = 400
            ws = root.winfo_screenwidth() # width of the screen
            hs = root.winfo_screenheight() # height of the screen
            x = (ws/2) - (w/2)
            y = (hs/2) - (h/2)
            credits_window.geometry('%dx%d+%d+%d' % (w, h, x, y))

            self.credits_window = credits_window
            self.credits_window.configure(bg='#625772')
            self.credits_image = tk.PhotoImage(file=resource_path("gui_element_graphics\\splash_screen\\splashScreen.png"))
            self.credits_canvas = Canvas(self.credits_window, width=300, height=400, bd=0, bg='#625772', highlightthickness=0, relief='ridge')
            self.credits_canvas.grid(row=0, column=0, sticky='nswe')
            self.credits_canvas.grid_propagate(True)
            self.credits_canvas.create_image(0, 15, anchor=NW, image=self.credits_image)

            self.close_button = tk.PhotoImage(file=resource_path("gui_element_graphics\\splash_screen\\close.png"))
            close_button = tk.Button(self.credits_window, image=self.close_button, relief=FLAT, bg='#625772', borderwidth=0, highlightthickness=0, command= lambda: credits_window.destroy())
            self.credits_canvas.create_window(287, 5, anchor=NW, window=close_button)

            versionNumber = self.credits_canvas.create_text(150,225,fill="#FFFFFF",font="Lato", text="version 4.0.1")
            self.credits_canvas.tag_raise(versionNumber)

            creditText = self.credits_canvas.create_text(150,250,fill="#FFFFFF",font="Lato", text="tool.box by James Allnutt")
            self.credits_canvas.tag_raise(creditText)

            helpButton = tk.Button(credits_window, command=lambda: self.open_help(),font="Lato", relief=FLAT, bg='#625772', fg="#FFFFFF", borderwidth=0, highlightthickness=0, text="Help Available Here.")
            self.credits_canvas.create_window(75,265, anchor=NW, window=helpButton)

            credits_window.mainloop()

    def open_help(self, *event):    
        webbrowser.open('https://opus2.freshdesk.com/')
        self.credits_window.destroy()

#Audio Management Tool

    def project_management_headers(self):
        self.save_management = tk.Frame(self.audio_tool_page, bg='#F6F6F6', width=226, height=400)
        self.save_management.grid(row=0, column=0)
        self.save_management.grid_propagate(False)

        header = tk.Label(self.save_management, text="Audio Projects", bg='#F6F6F6', fg='#69686D', font=('Helvetica', 12, 'bold'))
        header.grid(row=1, column=1, padx=(5,0), pady=(15), sticky=W)

    def project_management(self):
        global current_project_title_entry, current_project_recording_entry, current_project_date_entry, past_project_title_entry, past_project_date_entry, past_project_recording_entry, past_2_project_title_entry, past_2_project_date_entry, past_2_project_recording_entry

        self.project_info = tk.Frame(self.save_management)
        self.project_info.grid(row=4, column=1, columnspan=2, rowspan=1)
        self.project_info.grid_propagate(True)

        self.current_header_bg = tk.PhotoImage(file=resource_path('gui_element_graphics\\project_headers\\pink_header.png'))
        self.current_header_bg = self.current_header_bg.subsample(5,4)
        current_project_header = tk.Label(text="Current", bg='#F9A1BC', fg='#FFFFFF', font=('Helvetica', 9, 'bold'))
        current_project_header_canvas = Canvas(self.project_info, height=25, bg='#F6F6F6', bd=0, highlightthickness=0)
        current_project_header_canvas.grid(row=0, column=0, rowspan=1, sticky=NSEW)
        current_project_header_canvas.create_image(5, 0, anchor=NW, image=self.current_header_bg)
        current_project_header_canvas.create_window(20, 0, anchor=NW, window=current_project_header)

        current_project_title = tk.Label(text="Original File:", fg='#69686D', bg='#FFFFFF')
        current_project_date = tk.Label(text='Date:', fg='#69686D', bg='#FFFFFF')
        current_project_recording = tk.Label(text='Start Time:', fg='#69686D', bg='#FFFFFF')
        current_project_title_entry = tk.Label(text="N/A", fg='#69686D', bg='#FFFFFF')
        current_project_date_entry = tk.Label(text="N/A", fg='#69686D', bg='#FFFFFF')
        current_project_recording_entry = tk.Label(text="N/A", fg='#69686D', bg='#FFFFFF')

        self.plus_button = tk.PhotoImage(file=resource_path('gui_element_graphics\\buttons\\add_new.png'))
        save_button = tk.Button(self.save_management, image=self.plus_button, command=self.click_save_project)
        save_button.configure(bg='#F6F6F6', fg='#F6F6F6', height=18, width=16, borderwidth=0, highlightthickness=0, bd=0, relief=FLAT)

        self.project_background = tk.PhotoImage(file=resource_path('gui_element_graphics\\panels\\save_panels.png'))
        current_project_canvas = Canvas(self.project_info, bg='#F6F6F6', height=100, bd=0, highlightthickness=0)
        current_project_canvas.grid(row=1, column=0, sticky=NSEW)
        current_project_canvas.create_image(5, 0, anchor=NW, image=self.project_background)
        current_project_canvas.create_window(25, 15, anchor=NW, window=current_project_title)
        current_project_canvas.create_window(25, 35, anchor=NW, window=current_project_date)
        current_project_canvas.create_window(25, 55, anchor=NW, window=current_project_recording)
        current_project_canvas.create_window(100, 15, anchor=NW, window=current_project_title_entry)
        current_project_canvas.create_window(100, 35, anchor=NW, window=current_project_date_entry)
        current_project_canvas.create_window(100, 55, anchor=NW, window=current_project_recording_entry)
        current_project_canvas.create_window(200, 0, anchor=NW, window=save_button)

        self.past_header_bg = tk.PhotoImage(file=resource_path('gui_element_graphics\\project_headers\\purple_header.png'))
        self.past_header_bg = self.past_header_bg.subsample(5,4)
        past_project_header = tk.Label(text="Last Edits", bg='#A9BCEE', fg='#FFFFFF', font=('Helvetica', 9, 'bold'))
        past_project_header_canvas = Canvas(self.project_info, height=25, bg='#F6F6F6', bd=0, highlightthickness=0)
        past_project_header_canvas.grid(row=2, column=0, rowspan=1, sticky=NSEW)
        past_project_header_canvas.create_image(5, 0, anchor=NW, image=self.past_header_bg)
        past_project_header_canvas.create_window(15, 0, anchor=NW, window=past_project_header)

        past_project_title = tk.Label(text="Original File:", fg='#69686D', bg='#FFFFFF')
        past_project_date = tk.Label(text='Date:', fg='#69686D', bg='#FFFFFF')
        past_project_recording = tk.Label(text='Start Time:', fg='#69686D', bg='#FFFFFF')
        past_project_title_entry = tk.Label(text="No Save Set", fg='#69686D', bg='#FFFFFF')
        past_project_date_entry = tk.Label(text="No Save Set", fg='#69686D', bg='#FFFFFF')
        past_project_recording_entry = tk.Label(text="No Save Set", fg='#69686D', bg='#FFFFFF')

        load_button = tk.Button(self.save_management, image=self.plus_button)
        load_button.configure(bg='#F6F6F6', fg='#F6F6F6', height=18, width=16, borderwidth=0, highlightthickness=0, bd=0, relief=FLAT, command=self.click_previous_project_1)

        past_project_canvas = Canvas(self.project_info, bg='#F6F6F6', height=100, bd=0, highlightthickness=0)
        past_project_canvas.grid(row=3, column=0, sticky=NSEW)
        past_project_canvas.create_image(5, 0, anchor=NW, image=self.project_background)
        past_project_canvas.create_window(25, 15, anchor=NW, window=past_project_title)
        past_project_canvas.create_window(25, 35, anchor=NW, window=past_project_date)
        past_project_canvas.create_window(25, 55, anchor=NW, window=past_project_recording)
        past_project_canvas.create_window(100, 15, anchor=NW, window=past_project_title_entry)
        past_project_canvas.create_window(100, 35, anchor=NW, window=past_project_date_entry)
        past_project_canvas.create_window(100, 55, anchor=NW, window=past_project_recording_entry)
        past_project_canvas.create_window(200, 0, anchor=NW, window=load_button)

        past_2_project_title = tk.Label(text="Original File:", fg='#69686D', bg='#FFFFFF')
        past_2_project_date = tk.Label(text='Date:', fg='#69686D', bg='#FFFFFF')
        past_2_project_recording = tk.Label(text='Start Time:', fg='#69686D', bg='#FFFFFF')
        past_2_project_title_entry = tk.Label(text="No Save Set", fg='#69686D', bg='#FFFFFF')
        past_2_project_date_entry = tk.Label(text="No Save Set", fg='#69686D', bg='#FFFFFF')
        past_2_project_recording_entry = tk.Label(text="No Save Set", fg='#69686D', bg='#FFFFFF')

        load_2_button = tk.Button(self.save_management, image=self.plus_button)
        load_2_button.configure(bg='#F6F6F6', fg='#F6F6F6', height=18, width=16, borderwidth=0, highlightthickness=0, bd=0, relief=FLAT, command=self.click_previous_project_2)

        past_2_project_canvas = Canvas(self.project_info, bg='#F6F6F6', height=100, bd=0, highlightthickness=0)
        past_2_project_canvas.grid(row=4, column=0, sticky=NSEW)
        past_2_project_canvas.create_image(5, 0, anchor=NW, image=self.project_background)
        past_2_project_canvas.create_window(25, 15, anchor=NW, window=past_2_project_title)
        past_2_project_canvas.create_window(25, 35, anchor=NW, window=past_2_project_date)
        past_2_project_canvas.create_window(25, 55, anchor=NW, window=past_2_project_recording)
        past_2_project_canvas.create_window(100, 15, anchor=NW, window=past_2_project_title_entry)
        past_2_project_canvas.create_window(100, 35, anchor=NW, window=past_2_project_date_entry)
        past_2_project_canvas.create_window(100, 55, anchor=NW, window=past_2_project_recording_entry)
        past_2_project_canvas.create_window(200, 0, anchor=NW, window=load_2_button)

    def current_project_headers(self):
        global tools_canvas

        self.current_audio_project = tk.Frame(self.audio_tool_page, bg='#F6F6F6', height=400, width=462)
        self.current_audio_project.grid(row=0, column=1)
        self.current_audio_project.grid_propagate(False)

        project_header = tk.Label(text="Current", bg='#F9A1BC', fg='#FFFFFF', font=('Helvetica', 9, 'bold'))
        browse = tk.Label(text="Browse", bg='#FFFFFF', fg='#69686D', font=('Helvetica', 12, 'bold'))
        editing_header = tk.Label(text="Export Options", bg='#FFFFFF', fg='#69686D', font=('Helvetica', 12, 'bold'))

        self.tools_canvas_image = tk.PhotoImage(file=resource_path('gui_element_graphics\\panels\\project_tools.png'))

        tools_canvas = Canvas(self.current_audio_project, bg='#F6F6F6', bd=0, highlightthickness=0, height=340)
        tools_canvas.grid(row=1, column=1, columnspan=2, sticky=NSEW, pady=(10,0))
        tools_canvas.create_image(10, 0, anchor=NW, image=self.tools_canvas_image)
        tools_canvas.create_image(27, 15, anchor=NW, image=self.current_header_bg)
        tools_canvas.create_window(42, 15, anchor=NW, window=project_header)
        tools_canvas.create_window(27, 50, anchor=NW, window=browse)
        tools_canvas.create_window(27, 100, anchor=NW, window=editing_header)

    def current_project_tools(self):
        global progress, tools_canvas

        self.current_fp_background = tk.Label(bg='#F6F6F6', width=35)
        self.current_file_path = tk.Label(text="Click To Add Audio", bg='#FFFFFF', fg='#69686D', borderwidth=1, width=35)
        self.current_file_button = tk.PhotoImage(file=resource_path('gui_element_graphics\\buttons\\add_new.png'))
        current_file_button = tk.Button(image=self.current_file_button, width=17, command=self.click_browse, relief=FLAT, bg='#FFFFFF', borderwidth=0, highlightthickness=0)
  
        recordingDateLabel = tk.Label(self.current_audio_project, text="Sitting Date", bg='#FFFFFF', fg='#69686D')
        self.recording_date = tkc.DateEntry(self.current_audio_project, locale='en_GB', bg='#FFFFFF', fg='#69686D', relief="flat", highlightthickness=1)

        recordingStartTime = tk.Label(self.current_audio_project, text="Recording Start Time", bg='#FFFFFF', fg='#69686D')
        self.recording_start_time = tk.Entry(self.current_audio_project, bg='#FFFFFF', fg='#69686D', relief="flat", highlightthickness=1)
        self.recording_start_time.insert(0, "e.g. 09:41:00")
        calculator_button = tk.Button(image=self.current_file_button, width=17, command=self.open_calculator, relief=FLAT, bg='#FFFFFF', borderwidth=0, highlightthickness=0)

        audioChunkStartTime =  tk.Label(self.current_audio_project, text="Start Boundary", bg='#FFFFFF', fg='#69686D')
        self.recording_start_bound = tk.Entry(self.current_audio_project, bg='#FFFFFF', fg='#69686D', relief="flat", highlightthickness=1)
        self.recording_start_bound.insert(0, "e.g. 10:03:00")

        self.play_start = tk.PhotoImage(file=resource_path('gui_element_graphics\\buttons\\play.png'))
        recording_start_bound_play = tk.Button(self.current_audio_project, image=self.play_start, height=15, width=17, command=self.click_play_start, relief=FLAT, bg='#FFFFFF', borderwidth=0, highlightthickness=0)

        audioChunkEndTime = tk.Label(self.current_audio_project, text="End Boundary", bg='#FFFFFF', fg='#69686D')
        self.recording_end_bound = tk.Entry(self.current_audio_project, bg='#FFFFFF', fg='#69686D', relief="flat", highlightthickness=1)
        self.recording_end_bound.insert(0, "e.g. 12:30:21")

        self.play_end = tk.PhotoImage(file=resource_path('gui_element_graphics\\buttons\\play.png'))
        recording_end_bound_play = tk.Button(self.current_audio_project, image=self.play_end, height=15, width=17, command=self.click_play_end, relief=FLAT, bg='#FFFFFF', borderwidth=0, highlightthickness=0)

        audioFileNamePrefix = tk.Label(self.current_audio_project, text="Filename Prefix", bg='#FFFFFF', fg='#69686D')
        self.recording_file_prefix = tk.Entry(self.current_audio_project, bg='#FFFFFF', fg='#69686D', relief="flat", highlightthickness=1)
        self.recording_file_prefix.insert(0, "e.g. EventName")

        self.export_button = tk.PhotoImage(file=resource_path('gui_element_graphics\\buttons\\export.png'))
        export = tk.Button(self.current_audio_project, image=self.export_button, command=self.click_save, relief=FLAT, bg='#FFFFFF', borderwidth=0, highlightthickness=0)

        self.reset_button = tk.PhotoImage(file=resource_path('gui_element_graphics\\buttons\\reset.png'))
        reset = tk.Button(self.current_audio_project, image=self.reset_button, command=self.click_reset, relief=FLAT, bg='#FFFFFF', borderwidth=0, highlightthickness=0)

        tools_canvas.create_window(26, 74, anchor=NW, window=self.current_fp_background)

        tools_canvas.create_window(27, 75, anchor=NW, window=self.current_file_path)
        tools_canvas.create_window(282, 73, anchor=NW, window=current_file_button)

        tools_canvas.create_window(27, 140, anchor=NW, window=recordingDateLabel)
        tools_canvas.create_window(152, 140, anchor=NW, window=self.recording_date)

        tools_canvas.create_window(27, 170, anchor=NW, window=recordingStartTime)
        tools_canvas.create_window(152, 170, anchor=NW, window=self.recording_start_time)
        tools_canvas.create_window(282, 169, anchor=NW, window=calculator_button)

        tools_canvas.create_window(27, 200, anchor=NW, window=audioChunkStartTime)
        tools_canvas.create_window(152, 200, anchor=NW, window=self.recording_start_bound)
        tools_canvas.create_window(282, 202, anchor=NW, window=recording_start_bound_play)

        tools_canvas.create_window(27, 230, anchor=NW, window=audioChunkEndTime)
        tools_canvas.create_window(152, 230, anchor=NW, window=self.recording_end_bound)
        tools_canvas.create_window(282, 232, anchor=NW, window=recording_end_bound_play)

        tools_canvas.create_window(27, 260, anchor=NW, window=audioFileNamePrefix)
        tools_canvas.create_window(152, 260, anchor=NW, window=self.recording_file_prefix)

        tools_canvas.create_window(322, 287, anchor=NW, window=export)
        tools_canvas.create_window(26, 287, anchor=NW, window=reset)

        
        progress = ttk.Progressbar(self.current_audio_project, orient = HORIZONTAL, length = 20, style='Horizontal.TProgressbar')
        progress.config(mode='determinate', maximum=99.99, value=0)
        progress.grid(row=2, column=1, columnspan=2, sticky='nwe', padx=(20,8), pady=(10,0))

    def key_bindings(self):
        self.recording_start_time.bind("<FocusIn>", self.recording_start_time_click)
        self.recording_start_time.bind("<FocusOut>", self.recording_start_time_out_focus)

        self.recording_start_bound.bind("<FocusIn>", self.recording_start_bound_click)
        self.recording_start_bound.bind("<FocusOut>", self.recording_start_bound_out_focus)

        self.recording_end_bound.bind("<FocusIn>", self.recording_end_bound_click)
        self.recording_end_bound.bind("<FocusOut>", self.recording_end_bound_out_focus)
        
        self.recording_file_prefix.bind("<FocusIn>", self.recording_file_prefix_click)
        self.recording_file_prefix.bind("<FocusOut>", self.recording_file_prefix_out_focus)

    def recording_start_time_click(self, event):
        if self.recording_start_time.get() == "e.g. 09:41:00":
            self.recording_start_time.delete(0, "end")

    def recording_start_time_out_focus(self, event):
        if self.recording_start_time.get() == "":
            self.recording_start_time.insert(0, "e.g. 09:41:00")

    def recording_start_bound_click(self, event):
        if self.recording_start_bound.get() == "e.g. 10:03:00":
            self.recording_start_bound.delete(0, "end")

    def recording_start_bound_out_focus(self, event):
        if self.recording_start_bound.get() == "":
            self.recording_start_bound.insert(0, "e.g. 10:03:00")

    def recording_end_bound_click(self, event):
        if self.recording_end_bound.get() == "e.g. 12:30:21":
            self.recording_end_bound.delete(0, "end")

    def recording_end_bound_out_focus(self, event):
        if self.recording_end_bound.get() == "":
            self.recording_end_bound.insert(0, "e.g. 12:30:21")

    def recording_file_prefix_click(self, event):
        if self.recording_file_prefix.get() == "e.g. EventName":
            self.recording_file_prefix.delete(0, "end")

    def recording_file_prefix_out_focus(self, event):
        if self.recording_file_prefix.get() == "":
            self.recording_file_prefix.insert(0, "e.g. EventName")

    def click_browse(self, *event):
        global originalAudio, fileDisplay
        originalAudio = filedialog.askopenfilename(title = "Select WAV/WMA/MPEG/MP4 file",filetypes = (("WAV Files","*.wav"),("WMA files","*.wma"),("MPEG files","*.mpeg"),("MP4 files","*.mp4"),("all files","*.*")))
        fileDisplay = originalAudio.split("/")[-1]
        self.current_file_path.configure(text=fileDisplay, justify=LEFT)

    def click_save(self, *event):
        global progress

        startTime = self.recording_start_time.get()
        segmentStart = self.recording_start_bound.get()
        segmentEnd = self.recording_end_bound.get()
        sittingDate = self.recording_date.get()
        filePrefix =  self.recording_file_prefix.get()

        start_hour, start_minute, start_second = startTime.split(":")
        start_seg_hour, start_seg_minute, start_seg_second = segmentStart.split(":")
        end_hour, end_minute, end_second = segmentEnd.split(":")
        sitting_day, sitting_month, sitting_year = sittingDate.split("/")
        epoch_time_hour, epoch_time_minute, epoch_time_second = segmentStart.split(":")

        date_time = sittingDate + " " + segmentStart
        pattern = "%d/%m/%Y %H:%M:%S"
        getEpochTime = datetime.datetime.strptime(date_time, '%d/%m/%Y %H:%M:%S')
        epochTimeWithSeconds = getEpochTime.timestamp()
        savingsCheck = time.localtime(epochTimeWithSeconds).tm_isdst
        if savingsCheck == 1:
            epochTimeWithSeconds = epochTimeWithSeconds + 3600
            epochInteger, epochIgnore = str(epochTimeWithSeconds).split(".")
            convertTimeToWindowsMilli = (int(epochInteger)+11644473600)*10000000
            converted_time = hex(convertTimeToWindowsMilli)
            converted_time = "0" + str(converted_time[2:])
        else:
            epochInteger, epochIgnore = str(epochTimeWithSeconds).split(".")
            convertTimeToWindowsMilli = (int(epochInteger)+11644473600)*10000000
            converted_time = hex(convertTimeToWindowsMilli)
            converted_time = "0" + str(converted_time[2:])
    
        self.start_time_calc = int(start_hour)*3600 + int(start_minute)*60 + int(start_second)
        self.start_segment_time_calc = int(start_seg_hour)*3600 + int(start_seg_minute)*60 + int(start_seg_second)
        self.end_time_calc = int(end_hour)*3600 + int(end_minute)*60 + int(end_second)

        actual_start_segment = float(self.start_segment_time_calc) - float(self.start_time_calc)
        actual_end_segment = float(self.end_time_calc) - float(self.start_time_calc)
        target_file_duration = float(actual_end_segment) - float(actual_start_segment)

        self.savelocation = filedialog.askdirectory(title = "Save Location")
        new_filename = self.savelocation + "/" + str(filePrefix) + "_" + str(sitting_year) + str(sitting_month) + str(sitting_day) + "-" + str(epoch_time_hour) + str(epoch_time_minute) + "_" + str(converted_time) + ".wma"
        ffmpeg_command = FFmpeg(
            inputs={originalAudio: None},
            outputs={new_filename: ['-ss', str(actual_start_segment), '-to', str(actual_end_segment), '-async', '1', '-strict', '-2', '-ar', '44100', '-ab', '56k', '-ac', '1', '-y']}
        )
        command = ffmpeg_command.cmd
        Thread(target=lambda: progress_bar_percent(command, target_file_duration, lambda x: progress.config(value=x*100))).start()

    def click_play_start(self, *event):
        startTime = self.recording_start_time.get()
        segmentStart = self.recording_start_bound.get()

        start_hour, start_minute, start_second = startTime.split(":")
        start_seg_hour, start_seg_minute, start_seg_second = segmentStart.split(":")

        self.start_time_calc = int(start_hour)*3600 + int(start_minute)*60 + int(start_second)
        self.start_segment_time_calc = int(start_seg_hour)*3600 + int(start_seg_minute)*60 + int(start_seg_second)

        actual_start_segment = float(self.start_segment_time_calc) - float(self.start_time_calc)
        ffplay_path = resource_path("tools\\ffplay.exe")
        command_play = [ffplay_path, originalAudio, "-ss", str(actual_start_segment), "-t", "10", "-nodisp", "-autoexit"]
        Thread(target=lambda: play_beginning(command_play)).start()

    def click_play_end(self, *event):
        startTime = self.recording_start_time.get()
        start_hour, start_minute, start_second = startTime.split(":")
        self.start_time_calc = int(start_hour)*3600 + int(start_minute)*60 + int(start_second)

        segmentEnd = self.recording_end_bound.get()
        end_hour, end_minute, end_second = segmentEnd.split(":")
        self.end_time_calc = int(end_hour)*3600 + int(end_minute)*60 + int(end_second)

        end_segment = float(self.end_time_calc) - float(self.start_time_calc)
        actual_end_segment = float(end_segment) - 10 #taking away 10 seconds from end segment
        ffplay_path = resource_path("tools\\ffplay.exe")
        command_play = [ffplay_path, originalAudio, "-ss", str(actual_end_segment), "-t", "10", "-nodisp", "-autoexit"]
        Thread(target=lambda: play_end(command_play)).start()

    def click_reset(self, *event):
        self.recording_start_bound.delete(0,'end')
        self.recording_end_bound.delete(0,'end')
        self.recording_start_bound.insert(0, "e.g. 10:03:00")
        self.recording_end_bound.insert(0, "e.g. 12:30:21")
        progress.config(value=0)
 
    def click_save_project(self, *event):
        global originalAudio

        startTime = self.recording_start_time.get()
        sittingDate = self.recording_date.get()
        filePrefix =  self.recording_file_prefix.get()

        current_project_title_entry.configure(text=filePrefix)
        current_project_date_entry.configure(text=sittingDate)
        current_project_recording_entry.configure(text=startTime)
        
        save_path = os.path.join(os.path.expandvars("%userprofile%"),"Documents","ProductionAudioManagement.dat")
        save_file = [filePrefix, sittingDate, startTime, originalAudio]

        if os.path.getsize(save_path) > 0:
            with open(save_path, "rb") as file:
                append_save_file = [filePrefix, sittingDate, startTime, originalAudio]
                saved_content = pickle.Unpickler(file)
                load_file = saved_content.load()
                print(load_file)
                if len(load_file) == 8:
                    del load_file[4 : 8]
                    print(load_file)
                if len(load_file) == 4:
                    new_save = append_save_file + load_file
                    print(new_save)
                    pickle.dump(new_save, open(save_path, "wb"))
        else:
            pickle.dump(save_file, open(save_path, "wb"))

    def click_previous_project_1(self, *event):
        global originalAudio, fileDisplay
        save_path = os.path.join(os.path.expandvars("%userprofile%"),"Documents","ProductionAudioManagement.dat")
        with open(save_path, "rb") as file:
            saved_content = pickle.Unpickler(file)
            load_project_1 = saved_content.load()
        originalAudio = str(load_project_1[3])
        fileDisplay = originalAudio.split("/")[-1]
        self.current_file_path.configure(text=fileDisplay, justify=LEFT)
        sittingDate = str(load_project_1[1])
        self.recording_date.set_date(sittingDate)
        startTime = str(load_project_1[2])
        self.recording_start_time.delete(0,'end')
        self.recording_start_time.insert(0,startTime)
        filePrefix = str(load_project_1[0])
        self.recording_file_prefix.delete(0,'end')
        self.recording_file_prefix.insert(0,filePrefix)

    def click_previous_project_2(self, *event):
        global originalAudio, fileDisplay
        save_path = os.path.join(os.path.expandvars("%userprofile%"),"Documents","ProductionAudioManagement.dat")
        with open(save_path, "rb") as file:
            saved_content = pickle.Unpickler(file)
            load_project_1 = saved_content.load()
        originalAudio = str(load_project_1[7])
        fileDisplay = originalAudio.split("/")[-1]
        self.current_file_path.configure(text=fileDisplay, justify=LEFT)
        sittingDate = str(load_project_1[5])
        self.recording_date.set_date(sittingDate)
        startTime = str(load_project_1[6])
        self.recording_start_time.delete(0,'end')
        self.recording_start_time.insert(0,startTime)
        filePrefix = str(load_project_1[4])
        self.recording_file_prefix.delete(0,'end')
        self.recording_file_prefix.insert(0,filePrefix)

    def load_previous_projects_on_launch(self, *event):
        global originalAudio, load_project_1
        save_path = os.path.join(os.path.expandvars("%userprofile%"),"Documents","ProductionAudioManagement.dat")
        if not os.path.exists(save_path):
            with open (save_path, "w"):
                pass
        if os.path.getsize(save_path) > 0:
            with open(save_path, "rb") as file:
                saved_content = pickle.Unpickler(file)
                load_project_1 = saved_content.load()
                past_project_title_entry.configure(text=load_project_1[0])
                past_project_date_entry.configure(text=load_project_1[1])
                past_project_recording_entry.configure(text=load_project_1[2])
                past_2_project_title_entry.configure(text=load_project_1[4])
                past_2_project_date_entry.configure(text=load_project_1[5])
                past_2_project_recording_entry.configure(text=load_project_1[6])

    def open_calculator(self):
        calculator_window = Toplevel(root)
        self.calculator_window = calculator_window
        self.calculator_window.title("Timestamp Calculator")
        self.calculator_window.iconbitmap(resource_path("app_icon.ico"))
        self.calculator_window.configure(bg='#FFFFFF')

        tutorial = tk.Text(self.calculator_window, height=7, bg='#FFFFFF', highlightthickness=0, bd=0)
        tutorial.grid(row=0, column=1, columnspan=4, rowspan=1, sticky=NSEW, pady=(0,10))
        tutorial.tag_configure("allText", justify=CENTER, background='#FFFFFF', foreground='#69686D', font=('Helvetica', 9, 'bold'))
        tutorial_text = """ 
        This is a quick tool to calculate the
        start time of a recording for you. Listen to the raw audio,
        find the time elapsed which matches the first line spoken in
        the transcript, then put the time elapsed value into "Time Elapsed"
        below, and the actual timestamp from the first spoken line in the
        transcript into the "First Timestamp" below.
        """
        tutorial.insert(tk.END, tutorial_text, "allText")

        time_elapsed_label = tk.Label(self.calculator_window, text="Time Elapsed in Audio File:",bg='#FFFFFF', fg='#69686D', font=('Helvetica', 9, 'bold'))
        time_elapsed_label.grid(row=1, column=1)
        self.time_elapsed_entry = tk.Entry(self.calculator_window, bg='#FFFFFF', fg='#69686D', relief="flat", highlightthickness=1)
        self.time_elapsed_entry.grid(row=1, column=2)
        self.time_elapsed_entry.insert(0,"e.g. 01:42:36")
        first_transcript_time = tk.Label(self.calculator_window, text="First Timestamp in Transcript:",bg='#FFFFFF', fg='#69686D', font=('Helvetica', 9, 'bold'))
        first_transcript_time.grid(row=1, column=3)
        self.first_transcript_time_entry = tk.Entry(self.calculator_window, bg='#FFFFFF', fg='#69686D', relief="flat", highlightthickness=1)
        self.first_transcript_time_entry.grid(row=1, column=4)
        self.first_transcript_time_entry.insert(0,"e.g. 10:30:00")

        self.time_elapsed_entry.bind("<FocusIn>", self.time_elapsed_click)
        self.time_elapsed_entry.bind("<FocusOut>", self.time_elapsed_out_focus)
        self.first_transcript_time_entry.bind("<FocusIn>", self.first_transcript_time_click)
        self.first_transcript_time_entry.bind("<FocusOut>", self.first_transcript_time_out_focus)

        convert_canvas = Canvas(self.calculator_window, bg='#FFFFFF', bd=0, highlightthickness=0, height=70)
        convert_canvas.grid(row=2, column=1, columnspan=4, sticky=NSEW, pady=(5))
        self.convert_button = tk.PhotoImage(file=resource_path('gui_element_graphics\\buttons\\Convert.png'))
        convert_button = tk.Button(self.calculator_window, image=self.convert_button, command=self.calculator_start, relief=FLAT, bg='#FFFFFF', borderwidth=0, highlightthickness=0)
        convert_canvas.create_window(275, 0, anchor=NW, window=convert_button)

        calculator_window.mainloop()

    def calculator_start(self, *event):
        transcript_Time = self.first_transcript_time_entry.get()
        time_to_subtract = self.time_elapsed_entry.get()

        time_subtract_hour, time_subtract_minute, time_subtract_second = time_to_subtract.split(":")
        self.time_subtract = int(time_subtract_hour)*3600 + int(time_subtract_minute)*60 + int(time_subtract_second)

        transcript_hour, transcript_minute, transcript_second = transcript_Time.split(":")
        self.transcript_time = int(transcript_hour)*3600 + int(transcript_minute)*60 + int(transcript_second)

        calc = float(self.transcript_time) - float(self.time_subtract)
        new_time = time.strftime('%H:%M:%S', time.gmtime(calc))

        self.recording_start_time.delete(0, END)
        self.recording_start_time.insert(0, new_time)

        self.calculator_window.destroy()
        self.calculator_window.update()

    def time_elapsed_click(self, event):
        if self.time_elapsed_entry.get() == "e.g. 01:42:36":
            self.time_elapsed_entry.delete(0, "end")

    def time_elapsed_out_focus(self, event):
        if self.time_elapsed_entry.get() == "":
            self.time_elapsed_entry.insert(0, "e.g. 01:42:36")

    def first_transcript_time_click(self, event):
        if self.first_transcript_time_entry.get() == "e.g. 10:30:00":
            self.first_transcript_time_entry.delete(0, "end")

    def first_transcript_time_out_focus(self, event):
        if self.first_transcript_time_entry.get() == "":
            self.first_transcript_time_entry.insert(0, "e.g. 10:30:00")

#File Management Tool

    def files_job_management(self):
        self.save_file_management = tk.Frame(self.file_tool_page, bg='#F6F6F6', width=226, height=400)
        self.save_file_management.grid(row=0, column=0)
        self.save_file_management.grid_propagate(False)

        file_header = tk.Label(self.save_file_management, text="Transcript Production", bg='#F6F6F6', fg='#69686D', font=('Helvetica', 12, 'bold'))
        file_header.grid(row=1, column=1, padx=(5,0), pady=(15), sticky=W)

    def project_file_management(self):
        global current_project_title_entry, current_project_recording_entry, current_project_date_entry, past_project_title_entry, past_project_date_entry, past_project_recording_entry, past_2_project_title_entry, past_2_project_date_entry, past_2_project_recording_entry

        self.project_file_info = tk.Frame(self.save_file_management)
        self.project_file_info.grid(row=4, column=1, columnspan=2, rowspan=1)
        self.project_file_info.grid_propagate(True)

        self.current_file_header_bg = tk.PhotoImage(file=resource_path('gui_element_graphics\\project_headers\\pink_header.png'))
        self.current_file_header_bg = self.current_file_header_bg.subsample(5,4)
        current_project_file_header = tk.Label(text="Current", bg='#F9A1BC', fg='#FFFFFF', font=('Helvetica', 9, 'bold'))
        current_project_file_header_canvas = Canvas(self.project_file_info, height=25, bg='#F6F6F6', bd=0, highlightthickness=0)
        current_project_file_header_canvas.grid(row=0, column=0, rowspan=1, sticky=NSEW)
        current_project_file_header_canvas.create_image(5, 0, anchor=NW, image=self.current_file_header_bg)
        current_project_file_header_canvas.create_window(20, 0, anchor=NW, window=current_project_file_header)

        current_project_file_title = tk.Label(text="Original File:", fg='#69686D', bg='#FFFFFF')
        current_project_file_date = tk.Label(text='Date:', fg='#69686D', bg='#FFFFFF')
        current_project_file_recording = tk.Label(text='Start Time:', fg='#69686D', bg='#FFFFFF')
        current_project_file_title_entry = tk.Label(text="N/A", fg='#69686D', bg='#FFFFFF')
        current_project_file_date_entry = tk.Label(text="N/A", fg='#69686D', bg='#FFFFFF')
        current_project_file_recording_entry = tk.Label(text="N/A", fg='#69686D', bg='#FFFFFF')

        self.plus_file_button = tk.PhotoImage(file=resource_path('gui_element_graphics\\buttons\\add_new.png'))
        file_save_button = tk.Button(self.save_file_management, image=self.plus_file_button)
        file_save_button.configure(bg='#F6F6F6', fg='#F6F6F6', height=18, width=16, borderwidth=0, highlightthickness=0, bd=0, relief=FLAT)

        self.file_project_background = tk.PhotoImage(file=resource_path('gui_element_graphics\\panels\\save_panels.png'))
        current_project_file_canvas = Canvas(self.project_file_info, bg='#F6F6F6', height=100, bd=0, highlightthickness=0)
        current_project_file_canvas.grid(row=1, column=0, sticky=NSEW)
        current_project_file_canvas.create_image(5, 0, anchor=NW, image=self.file_project_background)
        current_project_file_canvas.create_window(25, 15, anchor=NW, window=current_project_file_title)
        current_project_file_canvas.create_window(25, 35, anchor=NW, window=current_project_file_date)
        current_project_file_canvas.create_window(25, 55, anchor=NW, window=current_project_file_recording)
        current_project_file_canvas.create_window(100, 15, anchor=NW, window=current_project_file_title_entry)
        current_project_file_canvas.create_window(100, 35, anchor=NW, window=current_project_file_date_entry)
        current_project_file_canvas.create_window(100, 55, anchor=NW, window=current_project_file_recording_entry)
        current_project_file_canvas.create_window(200, 0, anchor=NW, window=file_save_button)

        self.file_past_header_bg = tk.PhotoImage(file=resource_path('gui_element_graphics\\project_headers\\purple_header.png'))
        self.file_past_header_bg = self.file_past_header_bg.subsample(5,4)
        past_file_project_header = tk.Label(text="Last Edits", bg='#A9BCEE', fg='#FFFFFF', font=('Helvetica', 9, 'bold'))
        past_file_project_header_canvas = Canvas(self.project_file_info, height=25, bg='#F6F6F6', bd=0, highlightthickness=0)
        past_file_project_header_canvas.grid(row=2, column=0, rowspan=1, sticky=NSEW)
        past_file_project_header_canvas.create_image(5, 0, anchor=NW, image=self.file_past_header_bg)
        past_file_project_header_canvas.create_window(15, 0, anchor=NW, window=past_file_project_header)

        past_file_project_title = tk.Label(text="Original File:", fg='#69686D', bg='#FFFFFF')
        past_file_project_date = tk.Label(text='Date:', fg='#69686D', bg='#FFFFFF')
        past_file_project_recording = tk.Label(text='Start Time:', fg='#69686D', bg='#FFFFFF')
        past_file_project_title_entry = tk.Label(text="No Save Set", fg='#69686D', bg='#FFFFFF')
        past_file_project_date_entry = tk.Label(text="No Save Set", fg='#69686D', bg='#FFFFFF')
        past_file_project_recording_entry = tk.Label(text="No Save Set", fg='#69686D', bg='#FFFFFF')

        load_file_button = tk.Button(self.project_file_info, image=self.plus_button)
        load_file_button.configure(bg='#F6F6F6', fg='#F6F6F6', height=18, width=16, borderwidth=0, highlightthickness=0, bd=0, relief=FLAT)

        past_file_project_canvas = Canvas(self.project_file_info, bg='#F6F6F6', height=100, bd=0, highlightthickness=0)
        past_file_project_canvas.grid(row=3, column=0, sticky=NSEW)
        past_file_project_canvas.create_image(5, 0, anchor=NW, image=self.file_project_background)
        past_file_project_canvas.create_window(25, 15, anchor=NW, window=past_file_project_title)
        past_file_project_canvas.create_window(25, 35, anchor=NW, window=past_file_project_date)
        past_file_project_canvas.create_window(25, 55, anchor=NW, window=past_file_project_recording)
        past_file_project_canvas.create_window(100, 15, anchor=NW, window=past_file_project_title_entry)
        past_file_project_canvas.create_window(100, 35, anchor=NW, window=past_file_project_date_entry)
        past_file_project_canvas.create_window(100, 55, anchor=NW, window=past_file_project_recording_entry)
        past_file_project_canvas.create_window(200, 0, anchor=NW, window=load_file_button)

        past_file_2_project_title = tk.Label(text="Original File:", fg='#69686D', bg='#FFFFFF')
        past_file_2_project_date = tk.Label(text='Date:', fg='#69686D', bg='#FFFFFF')
        past_file_2_project_recording = tk.Label(text='Start Time:', fg='#69686D', bg='#FFFFFF')
        past_file_2_project_title_entry = tk.Label(text="No Save Set", fg='#69686D', bg='#FFFFFF')
        past_file_2_project_date_entry = tk.Label(text="No Save Set", fg='#69686D', bg='#FFFFFF')
        past_file_2_project_recording_entry = tk.Label(text="No Save Set", fg='#69686D', bg='#FFFFFF')

        load_file_2_button = tk.Button(self.project_file_info, image=self.plus_button)
        load_file_2_button.configure(bg='#F6F6F6', fg='#F6F6F6', height=18, width=16, borderwidth=0, highlightthickness=0, bd=0, relief=FLAT)

        past_file_2_project_canvas = Canvas(self.project_file_info, bg='#F6F6F6', height=100, bd=0, highlightthickness=0)
        past_file_2_project_canvas.grid(row=4, column=0, sticky=NSEW)
        past_file_2_project_canvas.create_image(5, 0, anchor=NW, image=self.file_project_background)
        past_file_2_project_canvas.create_window(25, 15, anchor=NW, window=past_file_2_project_title)
        past_file_2_project_canvas.create_window(25, 35, anchor=NW, window=past_file_2_project_date)
        past_file_2_project_canvas.create_window(25, 55, anchor=NW, window=past_file_2_project_recording)
        past_file_2_project_canvas.create_window(100, 15, anchor=NW, window=past_file_2_project_title_entry)
        past_file_2_project_canvas.create_window(100, 35, anchor=NW, window=past_file_2_project_date_entry)
        past_file_2_project_canvas.create_window(100, 55, anchor=NW, window=past_file_2_project_recording_entry)
        past_file_2_project_canvas.create_window(200, 0, anchor=NW, window=load_file_2_button)

    def current_project_file_headers(self):
        global tPC_canvas

        self.current_file_project = tk.Frame(self.file_tool_page, bg='#F6F6F6', height=400, width=462)
        self.current_file_project.grid(row=0, column=1)
        self.current_file_project.grid_propagate(False)

        project_file_header = tk.Label(text="Current", bg='#F9A1BC', fg='#FFFFFF', font=('Helvetica', 9, 'bold'))

        self.tPC_canvas_image = tk.PhotoImage(file=resource_path('gui_element_graphics\\panels\\files_background.png'))

        tPC_canvas = Canvas(self.current_file_project, bg='#F6F6F6', bd=0, highlightthickness=0, height=390)
        tPC_canvas.grid(row=1, column=1, columnspan=2, sticky=NSEW, pady=(10,0))
        tPC_canvas.create_image(10, 0, anchor=NW, image=self.tPC_canvas_image)
        tPC_canvas.create_image(27, 15, anchor=NW, image=self.current_header_bg)
        tPC_canvas.create_window(42, 15, anchor=NW, window=project_file_header)

    def transcriptProductionConfig(self):
        global tPC_canvas

        #HeaderLabels
        tPC_browseTranscriptLabel = tk.Label(text="Browse", bg='#FFFFFF', fg='#69686D', font=('Helvetica', 12, 'bold'))
        tPC_pageSetupLabel = tk.Label(text="Page Setup", bg='#FFFFFF', fg='#69686D', font=('Helvetica', 12, 'bold'))
        tPC_headerandFootersLabel = tk.Label(text="Headers and Footers", bg='#FFFFFF', fg='#69686D', font=('Helvetica', 12, 'bold'))

        #HeaderLabels on Canvas
        tPC_canvas.create_window(27, 50, anchor=NW, window=tPC_browseTranscriptLabel)
        tPC_canvas.create_window(27, 100, anchor=NW, window=tPC_pageSetupLabel)
        tPC_canvas.create_window(27, 200, anchor=NW, window=tPC_headerandFootersLabel)

        #User Inputs
        tPC_filePrefix = tk.Entry(bg='#FFFFFF', fg='#69686D', relief="flat", highlightthickness=1)
        tPC_filePrefix.insert(0, "Filename Prefix")

        tPC_coverPage = tk.Entry(bg='#FFFFFF', fg='#69686D', relief="flat", highlightthickness=1)
        tPC_coverPage.insert(0, "Cover Page")

        tPC_fullPageFormat = tk.Button(text="Full Page",bg='#FFFFFF', fg='#69686D')
        tPC_condensedPageFormat = tk.Button(text="4x4 Pages",bg='#FFFFFF', fg='#69686D')

        tPC_headerLeft = tk.Text(width=15, height=2)
        tPC_headerCenter = tk.Text(width=15, height=2)
        tPC_headerRight = tk.Text(width=15, height=2)

        tPC_footerLeft = tk.Text(width=15, height=2)
        tPC_footerCenter = tk.Text(width=15, height=2)
        tPC_footerRight = tk.Text(width=15, height=2)

        #User Inputs on Canvas
        tPC_canvas.create_window(27, 140, anchor=NW, window=tPC_filePrefix)
        tPC_canvas.create_window(27, 170, anchor=NW, window=tPC_coverPage)
        tPC_canvas.create_window(210, 150, anchor=NW, window=tPC_fullPageFormat)
        tPC_canvas.create_window(270, 150, anchor=NW, window=tPC_condensedPageFormat)

if __name__ == "__main__":
    root = tk.Tk()
    w = 690
    h = 400
    ws = root.winfo_screenwidth() # width of the screen
    hs = root.winfo_screenheight() # height of the screen
    x = (ws/2) - (w/2)
    y = (hs/2) - (h/2)
    root.geometry('%dx%d+%d+%d' % (w, h, x, y))

    def resource_path(relative_path):
        base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
        return os.path.join(base_path, relative_path)
    main_window = Production_Tools(root)

    maincolour = '#625772'
    secondarycolour = '#F6F6F6'
    highlightcolour = '#FFFFFF'
    selectcolour = '#A9EEE6'
    
    style = ttk.Style(root)
    # Import the Notebook.tab element from the default theme
    style.element_create('Plain.Notebook.tab', "from", 'default')
    # Redefine the TNotebook Tab layout to use the new element
    #style.layout("TNotebook.Tab",
     #   [('Plain.Notebook.tab', {'children':
      #      [('Notebook.padding', {'side': 'top', 'children':
       #         [('Notebook.focus', {'side': 'top', 'children':
        #            [('Notebook.label', {'side': 'top', 'sticky': ''})],
         #       'sticky': 'nswe'})],
          #  'sticky': 'nswe'})],
        # 'sticky': 'nswe'})])
    style.layout("TNotebook.Tab", [])
    style.configure("TNotebook",tabposition='wn',background=maincolour,tabmargins=(0, 0, 0, 0),borderwidth=0, bordercolour=maincolour)
    #style.configure("TNotebook.Tab",[]) background=maincolour, padding=(0,10), sticky='e')
    style.map("TNotebook.Tab", background=[('selected',highlightcolour)])

    originalAudio = " "
    sittingDate = " "
    startTime = " "
    segmentStart = " "
    segmentEnd = " "
    filePrefix = " "

    nano_seconds = 0
    converted_time = 0

    root.mainloop()
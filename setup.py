import sys
from cx_Freeze import *

base = None
if (sys.platform == "win32"):
    base = "Win32GUI"

build_exe_options = {
    "include_files": ["audioControls.py", 
                        "progressBar.py",
                        "tools",
                        "gui_element_graphics",
                        "app_icon.ico",
                        "save_file"
                        ],
    "includes": ["tkinter", "threading", "ttkthemes", "queue", "subprocess", "functools", "ffmpy", "os", "pickle", "sys", "time", "datetime", "webbrowser", "json"]
}

build_msi_options = {
    "initial_target_dir": ["C:\Program Files\tool.box"],
    "shortcutName":["tool.box"],
    "shortcutDir":["DesktopFolder"]
}

setup(name='tool.box',
    version='4.0.1',
    author='James Allnutt',
    options={
        'build_exe': build_exe_options,
        'build_msi': build_msi_options
    },
    description='Production tool.box',
    executables=[
        Executable(
            "main.py",
            copyright="Copyright (C) James Allnutt 2020",
            icon="C:\\Users\\jallnutt\\OneDrive - Opus 2\\Documents\\GitHub\\Local Server Requests\\Python-Audio-File-Splicer\\app_icon.ico",
            shortcutName="tool.box",
            shortcutDir="DesktopFolder",
            base=base
            )
        ]
    )


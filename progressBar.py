##The functions within this file all are reading the output of the subprocess command run in main.py for FFMPEG. 
##We are extracting data to calculate information such as - end file size, current file size, the closer they are, the higher percentage completed etc
##This was produced with help from github contributor Kokadva

import subprocess
from functools import reduce
from subprocess import CREATE_NO_WINDOW

def extract_raw_timecode(chunk):
    return chunk[chunk.index(b'time='):chunk.index(b' bitrate')]

def to_seconds(timecode):
    x = 60
    def func(y):
        nonlocal x
        y *= x
        x *= 60
        return y
    l = list(reversed(list(map(float, timecode[timecode.index(b'=') + 1:].split(b':')))))
    return reduce(lambda a, b: func(b) + a, l)

# Function to execute once new progress log is found
def on_new_log(new_progress, target_file_length, on_percentage_callback_func):
    timecode = extract_raw_timecode(new_progress)
    seconds = to_seconds(timecode)
    on_percentage_callback_func(seconds / target_file_length)

def skip_prefix(p):
    prefix = b''
    while True:
        tmp_output = p.stderr.read(100)
        prefix += tmp_output
        if b'size=' in prefix:
            return prefix[prefix.index(b'size='):]

def contains_new_progress(_bytes):
    return _bytes.count(b'size=') > 1

def extract_progress(_bytes):
    return _bytes[_bytes.index(b'size='):_bytes.index(b'size=', _bytes.index(b'size=') + 1)], \
           _bytes[_bytes.index(b'size=', _bytes.index(b'size=') + 1):]

def extract_last_progress(_bytes):
    return _bytes[_bytes.index(b'size='):]


def get_progress_log(p, _bytes, on_new_progress_callback):
    result = []
    while True:
        tmp_output = p.stderr.read(50)
        if not tmp_output:
            break
        _bytes += tmp_output
        if contains_new_progress(_bytes):
            last_progress, _bytes = extract_progress(_bytes)
            result.append(last_progress)
            on_new_progress_callback(last_progress)
    last_progress = extract_last_progress(_bytes)
    result.append(last_progress)
    on_new_progress_callback(last_progress)
    return result


def get_duration(file_path):
    from moviepy.editor import VideoFileClip
    clip = VideoFileClip(file_path)
    return clip.duration


def progress_bar_percent(command, result_file_duration, percentage_callback_function):
    p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, bufsize=1, creationflags=CREATE_NO_WINDOW)
    # Skip all the output before the progress log
    leftover = skip_prefix(p)
    # Read progress log
    on_new_progress_callback = lambda x: on_new_log(x, result_file_duration, percentage_callback_function)
    progress_log = get_progress_log(p, leftover, on_new_progress_callback)
    # print(progress_log)
    p.stdout.close()
    p.wait()

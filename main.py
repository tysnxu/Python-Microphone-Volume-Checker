import sounddevice as sd
import numpy as np
import os


def set_window_size():
    os.system(f"mode con:cols={total_spaces + 5} lines=2")


def title(title_text):
    os.system(f"title {title_text}")


def print_sound(indata, outdata, frames, time, status):
    global loudest_volume

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~
    # FOLLOWING LINES OF CODE FROM:
    # https://stackoverflow.com/questions/40138031/
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~
    volume_norm = np.linalg.norm(indata)*10
    volume_int = int(volume_norm)
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~

    print(f"{volume_int} {'|' * volume_int}{' '*(max(total_spaces - volume_int, 0))}", end='\r')

    if loudest_volume < volume_int:
        loudest_volume = volume_int

        if loudest_volume > 50:
            title(f"MAX-{loudest_volume} - MIC WORKS")
        else:
            title(f"MAX-{loudest_volume}")


total_spaces = 100
loudest_volume = 0
set_window_size()

with sd.Stream(callback=print_sound):
    sd.sleep(15000)


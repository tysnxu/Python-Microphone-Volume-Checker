import sounddevice as sd
import numpy as np
import os


def set_window_size():
    os.system(f"mode con:cols={total_line_spaces + 5} lines=2")


def title(title_text):
    os.system(f"title {title_text}")


def display_information(sound_volume: int):
    global loudest_volume, previous_volume

    print()

    if loudest_volume < sound_volume:
        loudest_volume = sound_volume

        if loudest_volume > 50:
            title(f"MAX-{loudest_volume} - MIC WORKS")
        else:
            title(f"MAX-{loudest_volume}")

    # HAVE THE VOLUME DROP GRADUALLY
    if sound_volume > previous_volume:
        lerp_new_sound = sound_volume
    else:
        lerp_new_sound = int(previous_volume * 0.5 + sound_volume * 0.5)

    print(f"{sound_volume} {'|' * lerp_new_sound}{' '*(max(total_line_spaces - lerp_new_sound, 0))}", end='\r')
    previous_volume = sound_volume


def print_sound(indata, outdata, frames, time, status):

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~
    # FOLLOWING LINE OF CODE FROM:
    # https://stackoverflow.com/questions/40138031/
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~
    volume_norm = np.linalg.norm(indata)*10
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~

    volume_int = int(volume_norm)
    display_information(volume_int)


total_line_spaces = 100

previous_volume = 0

recent_loudest_volume = 0
loudest_volume = 0

# SCRIPT STARTS
set_window_size()

with sd.Stream(callback=print_sound):
    sd.sleep(15000)


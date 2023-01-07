import sounddevice as sd
import numpy as np
import os


def set_window_size():
    os.system(f"mode con:cols={total_line_spaces + 5} lines=2")


def title(title_text):
    os.system(f"title {title_text}")


def lerp(number_a: float, number_b: float, ratio: float):
    return int(number_a * ratio + number_b * (1 - ratio))


def display_information(new_volume: int):
    global loudest_volume, previous_volume

    if loudest_volume < new_volume:
        loudest_volume = new_volume

        if loudest_volume > 50:
            title(f"MAX-{loudest_volume} - MIC WORKS")
        else:
            title(f"MAX-{loudest_volume}")

    # HAVE THE VOLUME DROP GRADUALLY
    if new_volume > previous_volume:
        lerped_new_volume = new_volume
    else:
        lerped_new_volume = lerp(previous_volume, new_volume, 0.5)

    print(f"{lerped_new_volume} {'|' * lerped_new_volume}{' ' * (max(total_line_spaces - lerped_new_volume, 0))}", end='\r')
    previous_volume = new_volume


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


import sounddevice as sd
import numpy as np
import os


def set_window_size():
    os.system(f"mode con:cols={total_line_spaces + 20} lines=2")


def title(title_text):
    os.system(f"title {title_text}")


def lerp(number_a: float, number_b: float, ratio: float):
    return int(number_b * ratio + number_a * (1 - ratio))


def update_loudest_volume(new_volume: int):
    global loudest_expire, loudest_volume

    if loudest_volume < new_volume:
        loudest_volume = new_volume
        loudest_expire = 50

        if loudest_volume > 50:
            title(f"MAX-{loudest_volume} - MIC WORKS")
        else:
            title(f"MAX-{loudest_volume}")
    else:
        if loudest_expire != 0:
            loudest_expire -= 1
        else:
            loudest_volume = new_volume


def format_printed_volume_bar(new_volume: int, max_volume: int):
    string_start = f"{new_volume:03}"
    volume_area = '|' * new_volume

    blank_spaces = max(total_line_spaces - new_volume, 0)  # IF VOLUME LARGER THAN 100, THIS WILL NOT BE NEGATIVE
    blank_area = ' ' * blank_spaces

    # DISPLAY MAX INDICATOR
    if max_volume > new_volume:
        gap_size = max_volume - new_volume - 1
        gap_area = ' ' * gap_size

        blank_spaces = max(total_line_spaces - max_volume - 1, 0)
        blank_area = ' ' * blank_spaces

        blank_area = f"{gap_area}*{blank_area}"

    return f"{string_start} {volume_area}{blank_area}"


def display_information(new_volume: int):
    global previous_volume

    update_loudest_volume(new_volume)

    # HAVE THE VOLUME DROP GRADUALLY
    if new_volume > previous_volume:
        lerped_new_volume = new_volume
    else:
        lerped_new_volume = lerp(previous_volume, new_volume, 0.2)

    print(format_printed_volume_bar(lerped_new_volume, loudest_volume), end='\r')
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

loudest_volume = 0
loudest_expire = 0

# SCRIPT STARTS
set_window_size()

with sd.Stream(callback=print_sound):
    sd.sleep(15000)


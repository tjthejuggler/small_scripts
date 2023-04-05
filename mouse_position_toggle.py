#!/usr/bin/env python3

import os
import sys
import time
from Xlib import display

def get_mouse_position():
    data = display.Display().screen().root.query_pointer()._data
    return data["root_x"], data["root_y"]

def main():
    THRESHOLD = 1000  # Time in milliseconds to check if the other side was touched
    LEFT_SIDE_X = 10  # Adjust this value based on your screen dimensions
    RIGHT_SIDE_X = 1900  # Adjust this value based on your screen dimensions

    state = 0
    start_time = 0

    toggle_script_location = '~/projects/small_scripts/toggle_mouse.sh'
    toggle_script_location = os.path.expanduser(toggle_script_location)

    while True:
        x, y = get_mouse_position()

        if state == 0 and x <= LEFT_SIDE_X:
            state = 1
            start_time = time.time()

        elif state == 1 and x >= RIGHT_SIDE_X:
            state = 2

        elif state == 2 and x <= LEFT_SIDE_X:
            print("Left, Right, Left sides touched quickly!")
            # Run your KDE script here
            os.system("bash "+toggle_script_location)
            state = 0

        elif state == 0 and x >= RIGHT_SIDE_X:
            state = -1
            start_time = time.time()

        elif state == -1 and x <= LEFT_SIDE_X:
            state = -2

        elif state == -2 and x >= RIGHT_SIDE_X:
            print("Right, Left, Right sides touched quickly!")
            # Run your KDE script here
            os.system("bash "+toggle_script_location)
            state = 0

        if (state != 0) and (time.time() - start_time) * 1000 > THRESHOLD:
            state = 0

        time.sleep(0.01)

if __name__ == "__main__":
    main()


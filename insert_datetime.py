import datetime
import pyautogui


def insert_datetime():
    # get the current datetime in the desired format
    now = datetime.datetime.now().strftime("<%Y-%m-%d %H:%M:%S>")
    print(now)
    # type the datetime using the pyautogui module
    pyautogui.typewrite(now)

insert_datetime()
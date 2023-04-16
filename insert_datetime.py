import datetime
import pyautogui
import time

def insert_datetime():

    # get the current datetime in the desired format
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(now)
    time.sleep(1)
    # type the datetime using the pyautogui module
    pyautogui.typewrite(now)

insert_datetime()
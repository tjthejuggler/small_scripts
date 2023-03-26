from subprocess import Popen, PIPE
import subprocess
import pyperclip
import json
import datetime
import pyautogui
import time

def sendmessage(message):
    subprocess.Popen(['notify-send', message])
    return

def get_clipboard_text():
    return pyperclip.paste()

#use subrocess and xsel to get the clipboard contents
def get_primary_clipboard():
    p = Popen(['xsel', '-o'], stdin=PIPE, stdout=PIPE, stderr=PIPE)
    output, err = p.communicate()
    output = output.decode('utf-8')
    return output

def save_highlighted_text_to_file(text):
    filename = '/home/lunkwill/Documents/obsidian_note_vault/noteVault/tail/tododb.txt'
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    try:
        with open(filename, "r") as f:
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        data = {}

    data[timestamp] = text

    with open(filename, "w") as f:
        json.dump(data, f, indent=4)


file = '/home/lunkwill/Documents/obsidian_note_vault/noteVault/habitCounters/owed-todos/owed-todos.txt'

highlighted_text = get_primary_clipboard()

if highlighted_text:
    with open(file, 'r') as f:
        lines = f.readlines()

    counter = int(lines[0])
    counter += 1

    with open(file, 'w') as f:
        f.write(str(counter))

    save_highlighted_text_to_file(highlighted_text)
    sendmessage(str(counter) + " todos in the queue")

    pyautogui.press('delete')
    time.sleep(0.1)
    pyautogui.press('delete')
    time.sleep(0.1)
    pyautogui.press('delete')





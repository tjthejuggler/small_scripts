from subprocess import Popen, PIPE
import subprocess
import pyperclip
import json
import datetime
import pyautogui
import time
import os
from total_and_pending_habits import get_summary

def notify(message):
    msg = "notify-send ' ' '"+message+"'"
    os.system(msg)

def get_clipboard_text():
    return pyperclip.paste()

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

def main():
    highlighted_text = get_primary_clipboard()
    if highlighted_text:
        habitsdb_to_add_dir = '~/Documents/obsidian_note_vault/noteVault/habitsdb_to_add.txt'
        habitsdb_to_add_dir = os.path.expanduser(habitsdb_to_add_dir)
        with open(habitsdb_to_add_dir, 'r') as f:
            habitsdb_to_add = json.load(f)        
        habitsdb_to_add["Todos done"] += 1
        with open(habitsdb_to_add_dir, 'w') as f:
            json.dump(habitsdb_to_add, f, indent=4, sort_keys=True)
        notify(str(get_summary()))
        save_highlighted_text_to_file(highlighted_text)
        pyautogui.press('delete')
        time.sleep(0.3)
        pyautogui.press('delete')
        time.sleep(0.3)
        pyautogui.press('delete')
        time.sleep(1) #run the script to update the theme
        update_theme_script = '~/projects/tail/habits_kde_theme.py'
        update_theme_script = os.path.expanduser(update_theme_script)
        os.system('python3 '+update_theme_script)

if __name__ == "__main__":
    main()
from tkinter import * 
from tkinter import messagebox
import subprocess
import os
import json
import time
from total_and_pending_habits import get_summary

#this script will que up an 'owed posture'(a computer session with good posture to add to my phone habits) 
#   next time i unlock my phone i will get credit for having had done a todo item.

good_file = '/home/lunkwill/Documents/obsidian_note_vault/noteVault/habitCounters/good_posture.txt'
owed_good_file = '/home/lunkwill/Documents/obsidian_note_vault/noteVault/habitCounters/owed-todos/good_posture.txt'
bad_file = '/home/lunkwill/Documents/obsidian_note_vault/noteVault/habitCounters/posture-counters/bad_posture.txt'

def notify(message):
    msg = "notify-send ' ' '"+message+"'"
    os.system(msg)

def get_count(file):
    with open(file, 'r') as f:
        lines = f.readlines()
        f.close()    
    counter = int(lines[0])    
    return counter

def update_file():
    habitsdb_to_add_dir = '~/Documents/obsidian_note_vault/noteVault/habitsdb_to_add.txt'
    habitsdb_to_add_dir = os.path.expanduser(habitsdb_to_add_dir)
    with open(habitsdb_to_add_dir, 'r') as f:
        habitsdb_to_add = json.load(f)
    habitsdb_to_add["Good posture"] += 1
    with open(habitsdb_to_add_dir, 'w') as f:
        json.dump(habitsdb_to_add, f, indent=4, sort_keys=True)
    #run the script to update the theme
    time.sleep(1)
    notify(str(get_summary()))
    update_theme_script = '~/projects/tail/habits_kde_theme.py'
    update_theme_script = os.path.expanduser(update_theme_script)
    os.system('python3 '+update_theme_script)
    

root = Tk()
root.withdraw()
  
msg_box = messagebox.askquestion("askquestion", "Was your posture good?")
if msg_box == "yes":
    print("Good")
    update_file()
    root.destroy()
else:
    root.destroy()
    
root.mainloop() 
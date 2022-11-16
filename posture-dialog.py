from tkinter import * 
from tkinter import messagebox
import subprocess
import os

#this script will que up an 'owed posture'(a computer session with good posture to add to my phone habits) 
#   next time i unlock my phone i will get credit for having had done a todo item.

def sendmessage(message):
    msg = "notify-send ' ' '"+message+"'"
    os.system(msg)

good_file = '/home/lunkwill/Documents/obsidian_note_vault/noteVault/habitCounters/good_posture.txt'
owed_good_file = '/home/lunkwill/Documents/obsidian_note_vault/noteVault/habitCounters/owed-todos/good_posture.txt'
bad_file = '/home/lunkwill/Documents/obsidian_note_vault/noteVault/habitCounters/posture-counters/bad_posture.txt'

def get_count(file):
    with open(file, 'r') as f:
        lines = f.readlines()
        f.close()    
    counter = int(lines[0])    
    return counter

def update_file(posture_type):
    if posture_type == "good":
        file = owed_good_file
    else:
        file = bad_file
    counter = get_count(file)
    counter += 1
    with open(file, 'w') as f:
        f.write(str(counter))
        f.close()
    sendmessage("       "*2+str(get_count(good_file)+1) + " - GOOD        ")#                 " + str(get_count(bad_file)) + " - BAD")
  
root = Tk()
root.withdraw()
  
msg_box = messagebox.askquestion("askquestion", "Was your posture good?")
if msg_box == "yes":
    print("Good")
    update_file("good")
    root.destroy()
else:
    root.destroy()
    
root.mainloop() 
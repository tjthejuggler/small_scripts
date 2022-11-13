import subprocess

#this script will que up an 'owed todo' so that next time i unlock my phone i will get credit for having had done a todo item.

def sendmessage(message):
    subprocess.Popen(['notify-send', message])
    return

file = '/home/lunkwill/Documents/obsidian_note_vault/noteVault/habitCounters/owed-todos/owed-todos.txt'

with open(file, 'r') as f:
    lines = f.readlines()
    f.close()

counter = int(lines[0])
counter += 1

with open(file, 'w') as f:
    f.write(str(counter))
    f.close()

sendmessage(str(counter))
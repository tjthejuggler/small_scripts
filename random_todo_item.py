import os
import random
import datetime

random_todo_filepath = '~/Documents/obsidian_note_vault/noteVault/random_todo_item.txt'
random_todo_filepath = os.path.expanduser(random_todo_filepath)

with open(random_todo_filepath, 'r') as f:
    random_todo_text = f.read()

previous_checked_date = random_todo_text.split("\n\n")[0]
#first_time_checked_today = random_todo_text.split(" ")[1]
random_todo_item = random_todo_text.split("\n\n")[1]

todays_date = datetime.datetime.now().strftime("<%Y-%m-%d>")

#if(True):
if (todays_date != previous_checked_date):
    inbox_filepath = '~/Documents/obsidian_note_vault/noteVault/Inbox.md'
    inbox_filepath = os.path.expanduser(inbox_filepath)
    with open(inbox_filepath, 'r') as f:
        inbox = f.read()
    full_list = inbox.split("\n\n")
    random_todo_item = random.choice(full_list)
    with open(random_todo_filepath, 'w') as f:
        f.write(todays_date + "\n\n" + random_todo_item.strip())

def notify(message):
    msg = "notify-send ' ' '"+message+"'"
    os.system(msg)

notify("Random Todo Item:\n\n"+random_todo_item)
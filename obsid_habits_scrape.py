import os
import json

directory = '/home/lunkwill/Documents/obsidian_note_vault/noteVault/habitCounters'
json_dict = {}

for filename in os.listdir(directory):
    if filename.endswith('.txt'):
        name = filename[:-4] # Remove the .txt extension
        json_dict[name] = [0]

with open('output.json', 'w') as f:
    json.dump(json_dict, f, indent=4)

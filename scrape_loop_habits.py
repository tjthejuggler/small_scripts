import csv
import json
from datetime import datetime, timedelta
import os

input_dir = '/home/lunkwill/Documents/obsidian_note_vault/noteVault/loop_habits/'
output_file = 'output2.json'

# Create a top-level dictionary for all habits
all_habits = {}

# Loop through all subdirectories in the input directory
for root, dirs, files in os.walk(input_dir):
    for dir_name in dirs:
        
        # Extract the habit name from the directory name
        habit_name = dir_name[4:].replace(' ', '_').replace('.', '')
        print(habit_name)

        # Read the data from the CSV file for this habit
        data = {}
        with open(os.path.join(root, dir_name, 'Checkmarks.csv'), 'r') as f:
            reader = csv.reader(f)
            #next(reader) # Skip the header row
            for row in reader:
                print(habit_name, row[0])
                date_str = row[0]
                amount = float(row[1])
                date = datetime.strptime(date_str, '%Y-%m-%d').date()
                #divide amount by 1000 and round up to nearest integer
                if 3 > amount > 0:
                    amount = 1
                else:
                    amount = int(amount/1000 + 0.5)
                data[date] = amount

        date_data = {}
        with open(os.path.join(root, dir_name, 'Scores.csv'), 'r') as f:
            reader = csv.reader(f)
            next(reader) # Skip the header row
            for row in reader:
                date_str = row[0]
                date_data[date] = amount

        # Determine the date range and fill in missing dates with 0 values


        # start_date = min(date_data.keys())
        # end_date = max(date_data.keys())
        # if data.keys():
        print(habit_name, data.keys())
        start_date = min(data.keys())
        #make end_date be the current date
        end_date = datetime.now().date()

        #end_date = max(data.keys())
        date_range = [start_date + timedelta(days=x) for x in range((end_date-start_date).days + 1)]
        for date in date_range:
            if date not in data:
                data[date] = 0

        # Add the data for this habit to the all_habits dictionary
        all_habits[habit_name] = {}
        for date in sorted(data.keys()):
            date_str = date.strftime('%Y-%m-%d')
            all_habits[habit_name][date_str] = data[date]

# Write the all_habits dictionary to a JSON file
with open(output_file, 'w') as f:
    json.dump(all_habits, f, indent=4)

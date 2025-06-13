import json
import os

def get_summary():
    habitsdb_to_add_dir = '/home/twain/noteVault/habitsdb_to_add.txt'
    habitsdb_to_add_dir = os.path.expanduser(habitsdb_to_add_dir)
    with open(habitsdb_to_add_dir, 'r') as f:
        habitsdb_to_add = json.load(f)
    habitsdb_dir = '/home/twain/noteVault/habitsdb.txt'
    habitsdb_dir = os.path.expanduser(habitsdb_dir)
    today_total = 0
    with open(habitsdb_dir, 'r') as f:
        habitsdb = json.load(f)
    for key in habitsdb_to_add.keys(): #check to see if the habit is in the habitsdb, we had one called None
        print(key)
        latest_habit_value = 0
        if key in habitsdb:
            inner_dict = habitsdb[key]
            sorted_dates = sorted(inner_dict.keys(), reverse=True)
            latest_habit_value = inner_dict[sorted_dates[0]]
        current_habit_today = latest_habit_value + habitsdb_to_add[key]
        def adjust_habit_count(count, habit_name):
            if "Pushups" in habit_name:
                return round(count / 30)
            elif "Situps" in habit_name:
                return round(count / 50)
            elif "Squats" in habit_name:
                return round(count / 30)
            elif "Cold Shower" in habit_name:
                if count > 0 and count < 3:
                    count = 3
                return round(count / 3)
            else:
                return count
        today_total += adjust_habit_count(current_habit_today, key)
    result = "Total - " + str(today_total) + "\n"
    result += "Pending - \n"
    for key, value in habitsdb_to_add.items():
        if value > 0:
            result += f"{key}: {value}\n"
    return(result)

print(get_summary())
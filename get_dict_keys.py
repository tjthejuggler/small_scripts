import json

# Load dictionary from JSON file
with open('output2.json', 'r') as f:
    my_dict = json.load(f)

# # Get list of keys
# keys_list = list(my_dict.keys())

# print(keys_list)





old_keys = ['Articles_read', 'Program', 'Meditate', 'Juggling_tech', 'Podcasts_finished', 'Apnea_Walk', 'Juggle_break_record', 'Sleep_next_to_watch', 'No_immediate_morning_phone', 'Draw', 'Writing_session', 'Cold_shower', 'Music', 'Create_Anki', 'Good_posture', 'Videos_watched', 'Learn_health', 'Language_studied', 'Janki', 'Apnea_PRC', 'Anki_My_Dis', 'Situps', 'Questions_asked', 'UC_post', 'Dream_act', 'Pushups', 'ToDo', 'Apnea_sPB', 'Apnea_aPB', 'Cardio', 'Squats', 'Fun_Juggle']

#new_keys = ['article_read', 'programming_sessions', 'meditations', 'juggling_tech_sessions', 'podcast_finished', 'apnea_walked', 'juggling_record_broke', 'sleep_watch', 'early_phone', 'drew', 'writing_sessions', 'cold_shower_widget', 'music_listen', 'anki_created', 'good_posture', 'educational_video_watched', 'health_learned', 'language_studied', 'janki_used', 'apnea_practiced', 'anki_mydis_done', 'launch_situps_widget', 'question_asked', 'uc_post', 'dream_acted', 'launch_pushups_widget', 'todos_done', 'apnea_spb', 'apnea_apb', 'cardio_sessions', 'launch_squats_widget', 'fun_juggle']

new_keys2 = ['Article read', 'Programming sessions', 'Meditations', 'Juggling tech sessions', 'Podcast finished', 'Apnea walked', 'Juggling record broke', 'Sleep watch', 'Early phone', 'Drew', 'Writing sessions', 'Cold Shower Widget', 'Music listen', 'Anki created', 'Good posture', 'Educational video watched', 'Health learned', 'Language studied', 'Janki used', 'Apnea practiced', 'Anki mydis done', 'Launch Situps Widget', 'Question asked', 'UC post', 'Dream acted', 'Launch Pushups Widget', 'Todos done', 'Apnea spb', 'Apnea apb', 'Cardio sessions', 'Launch Squats Widget', 'Fun juggle']
# Create a dictionary to map old keys to new keys
key_map = {old_key: new_key for old_key, new_key in zip(old_keys, new_keys2)}


# Create a new dictionary with updated keys using a dictionary comprehension
new_dict = {key_map.get(key, key): value for key, value in my_dict.items()}

# Write the all_habits dictionary to a JSON file
with open('output_new', 'w') as f:
    json.dump(new_dict, f, indent=4)

import os
import set_wallpaper
import time

home = os.path.expanduser("~")

wallpaper_settings = home+"/Pictures/Wallpapers/wallpaper_settings.txt"

def get_previous_background():
    #open wallpaper_settings
    with open(wallpaper_settings, 'r') as f:
        #read the contents of wallpaper_settings as a list of strings
        settings = f.read().split('\n')    
    return settings[2]

set_wallpaper.set_wallpaper(get_previous_background())

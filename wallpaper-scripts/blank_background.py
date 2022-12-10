import os
import set_wallpaper
import time

home = os.path.expanduser("~")

folder = home+"/Pictures/Wallpapers/"

wallpaper_settings = home+"/Pictures/Wallpapers/wallpaper_settings.txt"


#make a key shortcut like this:
#bash -c "python3 /home/lunkwill/projects/small_scripts/blank_background.py"

def turn_random_background_off():
    #open wallpaper_settings
    with open(wallpaper_settings, 'r') as f:
        #read the contents of wallpaper_settings as a list of strings
        settings = f.read().split('\n')    
    settings[0] = 'False'
    #write settings to wallpaper_settings
    with open(wallpaper_settings, 'w') as f:
        f.write('\n'.join(settings))

set_wallpaper.set_wallpaper("file:///home/lunkwill/Pictures/blank.png")
turn_random_background_off()
time.sleep(3)
set_wallpaper.set_wallpaper("file:///home/lunkwill/Pictures/blank.png")
turn_random_background_off()

import os
import random
import time
import set_wallpaper

home = os.path.expanduser("~")

wallpaper_folder = home+"/Pictures/Wallpapers/"

wallpaper_settings = home+"/Pictures/Wallpapers/wallpaper_settings.txt"

#should_continue = True



def check_if_random_background_is_on():
    #open wallpaper_settings
    with open(wallpaper_settings, 'r') as f:
        #read the contents of wallpaper_settings as a list of strings
        settings = f.read().split('\n')    

    return settings[0] == 'True'

def main():
    
    should_continue = True
    while should_continue:
        
        #randomly run this function on average once per minute
        if random.randint(0, 1800) == 0 & check_if_random_background_is_on():
            set_wallpaper.set_random_wallpaper()
        #sleep for one second
        should_continue = check_if_random_background_is_on()
        time.sleep(1)
    
#os.system('gsettings set org.gnome.desktop.background picture-uri-dark "file:///home/lunkwill/Pictures/Wallpapers/frequency-spectrum.jpg"')




#whenever any program sets the background, it should save the filename to a textfile
#   but before that it should seve the current contents of the textfile to another textfile
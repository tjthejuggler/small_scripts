import os
import random
home = os.path.expanduser("~")

wallpaper_folder = home+"/Pictures/Wallpapers/"

wallpaper_settings = home+"/Pictures/Wallpapers/wallpaper_settings.txt"

def record_current_background(image):
    #open wallpaper_settings
    with open(wallpaper_settings, 'r') as f:
        #read the contents of wallpaper_settings as a list of strings
        settings = f.read().split('\n')    
    #get current background
    settings[2] = settings[1]
    #current_background = os.popen('gsettings get org.gnome.desktop.background picture-uri-dark').read()
    #write current background to wallpaper_settings
    settings[1] = image
    #write settings to wallpaper_settings
    with open(wallpaper_settings, 'w') as f:
        f.write('\n'.join(settings))

def turn_random_background_on():
    #open wallpaper_settings
    with open(wallpaper_settings, 'r') as f:
        #read the contents of wallpaper_settings as a list of strings
        settings = f.read().split('\n')    
    settings[0] = 'True'
    #write settings to wallpaper_settings
    with open(wallpaper_settings, 'w') as f:
        f.write('\n'.join(settings))

def set_wallpaper(image):
    #set ubuntu background to image
    record_current_background(image)
    os.system('gsettings set org.gnome.desktop.background picture-uri-dark "'+image+'"')

def set_random_wallpaper():
    #get home directory
    image = 'none.txt'
    turn_random_background_on()
    #while image is a .txt file
    while image[-4:] == '.txt' or image[-9:] == 'blank.png' or image[-9:] == '.stfolder':
        #randomly choose an image from the wallpaper_folder
        image = "file:///home/lunkwill/Pictures/Wallpapers/"+random.choice(os.listdir(wallpaper_folder))
    #image = 'baby.png'
    print(image)
    #set ubuntu background to image
    set_wallpaper(image)
    #os.system('gsettings set org.gnome.desktop.background picture-uri-dark "'+image+'"')

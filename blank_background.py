import os
import random

#make a key shortcut like this:
#bash -c "python3 /home/lunkwill/projects/small_scripts/blank_background.py"

#get home directory
home = os.path.expanduser("~")

folder = home+"/Pictures/Wallpapers/"
#randomly choose an image from the folder
image = "file:///home/lunkwill/Pictures/blank.png"


#image = 'baby.png'
print(image)
#set ubuntu background to image
os.system('gsettings set org.gnome.desktop.background picture-uri-dark "'+image+'"')
import os
import random

#get home directory
home = os.path.expanduser("~")

folder = home+"/Pictures/Wallpapers/"
#randomly choose an image from the folder
image = "file:///home/lunkwill/Pictures/Wallpapers/"+random.choice(os.listdir(folder))


#image = 'baby.png'
print(image)
#set ubuntu background to image
os.system('gsettings set org.gnome.desktop.background picture-uri-dark "'+image+'"')
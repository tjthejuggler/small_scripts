import os
import random
import set_wallpaper
import auto_random_background



#check if random background is on
if not auto_random_background.check_if_random_background_is_on():
    #if it is on, turn it off
    #auto_random_background.turn_random_background_off()
    #and start the auto_random_background script

    #make ubuntu notification
    #os.system('notify-send "Random Background" "Random background is now off"')
    set_wallpaper.turn_random_background_on()
    auto_random_background.main()

set_wallpaper.set_random_wallpaper()

# #get home directory
# home = os.path.expanduser("~")

# folder = home+"/Pictures/Wallpapers/"

# image = 'none.txt'

# #while image is a .txt file
# while image[-4:] == '.txt':
#     #randomly choose an image from the folder
#     image = "file:///home/lunkwill/Pictures/Wallpapers/"+random.choice(os.listdir(folder))

# #image = 'baby.png'
# print(image)
# #set ubuntu background to image
# os.system('gsettings set org.gnome.desktop.background picture-uri-dark "'+image+'"')




#whenever any program sets the background, it should save the filename to a textfile
#   but before that it should seve the current contents of the textfile to another textfile
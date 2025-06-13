#!/bin/bash
# Dependencies: tesseract-ocr imagemagick scrot xsel

SCR_IMG=`mktemp`
trap "rm $SCR_IMG*" EXIT

spectacle -b -s -o $SCR_IMG.png
# increase image quality with option -q from default 75 to 100

mogrify -modulate 100,100 -resize 200% -colorspace Gray -sharpen 0x1 -filter Lanczos $SCR_IMG.png
#should increase detection rate

tesseract -l eng $SCR_IMG.png $SCR_IMG
ls -l $SCR_IMG.txt
cat $SCR_IMG.txt | xsel -bi
echo "Copied to clipboard"

cp $SCR_IMG.png /tmp/screen.png
xdg-open /tmp/screen.png

exit

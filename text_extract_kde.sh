#!/bin/bash 
# Dependencies: tesseract-ocr imagemagick xsel

SCR_IMG=`mktemp`
trap "rm $SCR_IMG*" EXIT

import "$SCR_IMG.png"

mogrify -modulate 100,0 -resize 400% "$SCR_IMG.png"

tesseract "$SCR_IMG.png" "$SCR_IMG" &> /dev/null
cat "$SCR_IMG.txt" | xsel -bi

exit

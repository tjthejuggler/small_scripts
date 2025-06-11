#!/usr/bin/env python3
import datetime
import subprocess
import time

now = datetime.datetime.now()
datetime_string = now.strftime("%Y-%m-%d %H:%M:%S")

subprocess.run(['xdotool', 'type', '--clearmodifiers', datetime_string])
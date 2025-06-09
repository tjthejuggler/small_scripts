#!/usr/bin/env python3
import datetime
import sys

now = datetime.datetime.now()
print(now.strftime("%Y-%m-%d %H:%M:%S"), end="")
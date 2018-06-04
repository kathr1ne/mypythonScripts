#!/usr/bin/python
#
#

import os

def search(paths):
    if os.path.isdir(paths):
        files = os.listdir(paths)
        for i in files:
            i = os.path.join(paths, i)
            search(i)
    elif os.path.isfile(paths):
        print(paths)


search('/root/Bash')

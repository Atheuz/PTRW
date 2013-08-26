# -*- coding: utf-8 -*-

# Filename      main.py
# Author        Lasse Vang Gravesen <gravesenlasse@gmail.com>
# First edited  26-08-2013 04:13
# Last edited   26-08-2013 04:48

import argparse
import os
import sys
import shutil
import glob
from fabric.api import env
from fabric.operations import put
from fabric.main import load_settings

def run(files=None):
    if files is None:
        files_to_push = glob.glob("watch/*.torrent")
        for i in files_to_push:
            put(i, "private/deluge/watch")
            # Can't have the watch folder keep growing, so once a file has been put it is moved to the archive dir.
            shutil.move(i, "archive")
    else:
        for i in files:
            if os.path.isfile(i) and os.path.splitext(i)[1] == ".torrent":
                put(i, "private/deluge/watch")
                # Don't want to mess with files outside of the watch dir, so we copy instead.
                shutil.copy(i, "archive")
            elif os.path.isdir(i):
                files_to_push = glob.glob(os.path.join(i, "*.torrent"))
                for j in files_to_push:
                    put(j, "private/deluge/watch")
                    shutil.copy(j, "archive")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('files', metavar='f', type=str, nargs='*',
                        help='Set file or directory of files to push to watch.')
    args = parser.parse_args()

    env.rcfile = "fabricrc"
    env.update(load_settings(env.rcfile))

    if not os.path.isdir("watch"):
        os.mkdir("watch")
    if not os.path.isdir("archive"):
        os.mkdir("archive")
    
    if args.files:
        run(files=args.files)
    else:
        run()

if __name__ == '__main__':
    main()


#!/usr/bin/env python
import sys
from distutils.core import setup
sys.path.insert(0, 'lib')
from mpdrandom import PV

setup(
    name = "mpdrandom",
	package_dir = {'':'lib'},
    packages = ["mpdrandom"],
	scripts = ['mpdrandom'],
    version = PV,
    description = "mpd albums randomizing script",
    author = "Axujen",
    author_email = "axujen@gmail",
	url = "https://github.com/axujen/mpdrandom",
    keywords = ["mpd", "album", "random"],
    classifiers = [
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Development Status :: 4 - Beta",
        ],
    long_description = """\
mpdrandom
---------
A script that adds the missing randomness to mpds albums

Features
-Pick a random album from the playlist and play it
-Daemon mode: Play a random album when you reach the end of the current one.
-Shuffle: Shuffle all albums in the current playlist.
""",)

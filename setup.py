#!/usr/bin/env python3
from distutils.core import setup
from lib import PV

setup(name="mpdrandom",
      packages=["lib"],
      scripts=['mpdrandom'],
      version=PV,
      description="mpd albums randomizing script",
      author="Axujen",
      author_email="axujen (at) autistici.org",
      url="https://github.com/axujen/mpdrandom",
      keywords=["mpd", "album", "random", "shuffle", "music"],
      license="License :: OSI Approved :: GNU General Public License (GPL)",
      classifiers=[
          "Programming Language :: Python",
          "Development Status :: 4 - Beta",
      ],
    long_description="""\
mpdrandom
---------
A script that adds the missing randomness to mpds albums

Features
* Pick a random album from the playlist and play it
* Daemon mode: Play a random album when you reach the end of the current one.
* Shuffle: Shuffle all albums in the current playlist.
* *NEW* Play albums randomly from the library
""",)

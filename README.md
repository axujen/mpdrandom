mpdrandom
============
Is a script that adds some randomness to mpds albums.

NOTE: this script expects your music library to be properly tagged, personally on linux i use beets

# Features
* Pick a random album from the playlist and play it
* Daemon mode: Play a random album when you reach the end of the current one.
* Shuffle: Shuffle all albums in the current playlist.
* Play albums randomly from the library 
* Play albums randomly from a base directory
# Installation
	git clone git://github.com/axujen/mpdrandom.git
	cd mpdrandom
	sudo ./setup.py install
# Usage
    usage: mpdrandom [-h] [-d] [-l] [-c] [-z] [-p PORT] [-u HOST]
                     [--password PASSWORD] [-b BASE]
    
    Pick and play a random album from the current playlist
    
    optional arguments:
      -h, --help            show this help message and exit
      -d, --daemon          run the script in daemon mode.
      -l, --library         use the whole library instead of playlist.
      -c, --clear           clear the playlist before adding new album when using the
                            whole library
      -z, --shuffle         shuffle the albums in the current playlist.
      -p PORT, --port PORT  specify mpd's port (defaults to 6600)
      -u HOST, --host HOST  specify mpd's host (defaults to 127.0.0.1)
      --password PASSWORD   specify mpd's password
      -b BASE, --base BASE  specify base directory for adding from library
# Thanks
Thanks to [kmac](https://github.com/kmac/mpdscripts/blob/master/mpd-random-pl-album.py). His script inspired me to make my own.

Also for various [pull requests](https://github.com/axujen/mpdrandom/pulls?q=is%3Apr+is%3Aclosed):
* [cbumae](https://github.com/cbumae)
* [bi0ha2ard](https://github.com/bi0ha2ard)
* [vbabiy](https://github.com/vbabiy)
* [Polochon-street](https://github.com/Polochon-street)

mpdrandom
============
Is a script that adds some randomness to mpds albums.

# Features
* Pick a random album from the playlist and play it
* Daemon mode: Play a random album when you reach the end of the current one.
* Shuffle: Shuffle all albums in the current playlist.
* *NEW* Play albums randomly from the library 

#Installation
	git clone git://github.com/axujen/mpdrandom.git
	cd mpdrandom
	sudo ./setup.py install

#Usage
    usage: mpdrandom [-h] [-d] [-l] [-z] [-p PORT] [-u HOST] [--password PASSWORD]
    
    Pick and play a random album from the current playlist
    
    optional arguments:
      -h, --help            show this help message and exit
      -d, --daemon          run the script in daemon mode.
      -l, --library         use the whole library instead of playlist.
      -z, --shuffle         shuffle the albums in the current playlist.
      -p PORT, --port PORT  specify mpd's port (defaults to 6600)
      -u HOST, --host HOST  specify mpd's host (defaults to 127.0.0.1)
      --password PASSWORD   specify mpd's password

#Thanks
Thanks to [kmac](https://github.com/kmac/mpdscripts/blob/master/mpd-random-pl-album.py). His script inspired me to make my own.

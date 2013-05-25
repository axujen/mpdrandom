mpdrandom
============
Is a script that adds some randomness to mpds albums.

# Features
* Pick a random album from the playlist and play it
* Daemon mode: Play a random album when you reach the end of the current one.
* Shuffle: Shuffle all albums in the current playlist.

#Installation
	git clone git://github.com/axujen/mpdrandom.git
	cd mpdrandom
	sudo ./setup.py install

#Usage
run the script manually to play a random album from your playlist, or run it
with the --daemon flag to play a random album at the end of each album,
or with the --shuffle flag to shuffle the albums in the playlist.(see --help for more options)

#Thanks
Thanks to [kmac](https://github.com/kmac/mpdscripts/blob/master/mpd-random-pl-album.py). His script inspired me to make my own.

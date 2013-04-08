#!/usr/bin/env python3
# © Copyright 2013 axujen, <axujen at gmail.com>. All Rights Reserved.
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""This is a script to randomly select an album in the current mpd playlist."""

import random

try:
	import mpd
except ImportError:
	print('You must install the python-mpd2 library. You can get it from: '\
			'https://pypi.python.org/pypi?:action=display&name=python-mpd2')
	raise SystemExit

# Server info
MPD_ADDRESS = "127.0.0.1"
MPD_PORT = "6600"
PASSWORD = False
SERVER_ID = {"HOST":MPD_ADDRESS, "PORT":MPD_PORT}

class Client(mpd.MPDClient):
	"""Client that connects and communicates with the mpd server."""

	def __init__(self, server_id, password=False):
		mpd.MPDClient.__init__(self)
		self.connect(**server_id)
		self.iterate = True
		if password:
			self.password(password)

	def getalbums(self):
		"""Grab a list of the albums in the playlist."""
		albums = {}
		for song in self.playlistinfo():
			album = song['album']
			if not album in albums:
				albums[album] = [song]
			else:
				albums[album].append(song)

		return albums

	def getcurrent_album(self):
		"""Get the current playing album."""
		return self.currentsong()['album']

	def random_album(self, albums):
		"""Get a random album from the albums dictionary."""
		albums = list(albums.keys())
		# Everything except the current playing album
		current_album = self.getcurrent_album()
		albums.pop(albums.index(current_album))
		return random.choice(albums)

	def play_album(self, album):
		"""Play the given album."""
		self.playid(album[0]['id'])

	def play_random(self, albums):
		"""Play a random album from the list of albums."""
		if not albums:
			albums = self.getalbums()

		toplay = self.random_album(albums)
		self.play_album(albums[toplay])

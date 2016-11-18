#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# © Copyright 2013, 2016 axujen, <axujen at gmail.com>. All Rights Reserved.
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
    print('You must install the python-mpd2 library. You can get it from: '
          'https://pypi.python.org/pypi?:action=display&name=python-mpd2')
    raise SystemExit

# Default Server info, change these values to match yours.
HOST = '127.0.0.1'
PORT = '6600'
PASSWORD = None

__version__ = '1.2.0'
__author__ = 'Axujen'
__email__ = 'axujen@gmail.com'


class Client(mpd.MPDClient):
    """Client that connects and communicates with the mpd server."""

    def __init__(self, server_id, password=False):
        mpd.MPDClient.__init__(self)
        self.connect(**server_id)
        if password:
            self.password(password)

    def getalbums(self):
        """Grab a list of the albums in the playlist."""
        playlist = self.playlistinfo()
        albums = {}
        for song in playlist:
            try:
                album = song['album']
            except KeyError:
                album = 'None'
            if album not in albums:
                albums[album] = [song]
            else:
                albums[album].append(song)

        return albums

    def getcurrent_album(self):
        """Get the currently playing album."""
        try:
            album = self.currentsong()['album']
        except KeyError:
            album = None
        return album

    def random_album(self, albums):
        """Get a random album from the albums dictionary."""
        albums = list(albums.keys())
        # Everything except the current playing album
        current_album = self.getcurrent_album()
        if current_album:
            albums.pop(albums.index(current_album))
        if albums:
            return random.choice(albums)
        else:
            return None

    def play_album(self, album):
        """Play the first song in the given album."""
        song = album[0]
        print('Playing album "%s - %s".' % (song['artist'], song['album']))
        self.playid(song['id'])

    def play_random(self, lib=False):
        """Play a random album from the list of albums."""
        if not lib:  # Play from the playlist
            albums = self.getalbums()
            toplay = self.random_album(albums)
            if toplay:  # Make sure we found a random album
                self.play_album(albums[toplay])
            else:
                print("Nothing to play.")
        else:  # Play from the library
            album_name = random.choice(self.list('album'))  # Select a random album from the library
            if album_name:
                if album_name not in self.getalbums():  # Queue the album if not queued
                    self.findadd('album', album_name)

                album = self.getalbums()[album_name]
                self.play_album(album)

    def atlast_song(self):
        albums = self.getalbums()
        album = albums[self.getcurrent_album()]
        last_song = album[-1]['id']
        cursong = self.currentsong()['id']
        return True if last_song == cursong else False

    def idleloop(self, lib):
        """Loop for daemon mode."""
        while True:
            self.idle('player')
            if self.atlast_song():  # Started playing the last song
                self.idle('player')  # Wait for it to end
                self.play_random(lib)
            continue

    def move_album(self, album, pos=0):
        """Insert an album in the playlist."""
        for song in album:
            self.moveid(song['id'], pos)
            pos += 1

    def shuffle_albums(self):
        """Shuffle the albums in the playlist."""
        albums = self.getalbums()

        # Shuffle the albums
        album_names = list(albums.keys())
        random.shuffle(album_names)

        # Insert the new shuffled list
        for album in album_names:
            self.move_album(albums[album])

    def __del__(self):
        """Close client after exiting."""
        self.close()


def main():
    # Arguments
    from argparse import ArgumentParser
    arguments = ArgumentParser(description="Pick and play a random album from "
                               "the current playlist")
    arguments.add_argument('-d', '--daemon', action='store_true', dest='daemon',
                    help='run the script in daemon mode.', default=False)
    arguments.add_argument('-l', '--library', action='store_true', dest='library',
                          default=False, help='use the whole library instead of playlist.')
    arguments.add_argument('-z', '--shuffle', dest="shuffle", action='store_true',
                    default=False, help='shuffle the albums in the current playlist.')
    arguments.add_argument('-p', '--port', dest='port', default=PORT,
                    help='specify mpd\'s port (defaults to {})'.format(PORT), metavar='PORT')
    arguments.add_argument('-u', '--host', dest='host', default=HOST,
                    help='specify mpd\'s host (defaults to {})'.format(HOST), metavar='HOST')
    arguments.add_argument('--password', dest='password', default=PASSWORD,
                    help='specify mpd\'s password', metavar='PASSWORD')
    args = arguments.parse_args()

    SERVER_ID = {"host": args.host, "port": args.port}
    client = Client(SERVER_ID, args.password)
    if args.daemon:
        try:
            print("Going into daemon mode, press Ctrl-C to exit.")
            client.idleloop(lib=args.library)
        except KeyboardInterrupt:
            raise SystemExit  # No need for the ugly traceback when interrupting.
    elif args.shuffle:
        client.shuffle_albums()
        raise SystemExit
    else:
        client.play_random(lib=args.library)

if __name__ == '__main__':
    main()

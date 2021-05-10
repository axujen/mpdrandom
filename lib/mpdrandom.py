#!/usr/bin/env python3
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

from argparse import ArgumentParser
from mpd.asyncio import MPDClient
from mpd.base import VERSION
from threading import Thread
import asyncio
import random
import sys


# Default Server info, change these values to match yours.
HOST = '127.0.0.1'
PORT = '6600'
PASSWORD = None



class Client(MPDClient):
    """Client that connects and communicates with the mpd server."""

    def __init__(self, password=False):
        MPDClient.__init__(self)
        if password:
            self.password(password)

    async def getalbums(self):
        """Grab a list of the albums in the playlist."""
        playlist = await self.playlistinfo()
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

    async def getcurrent_album(self):
        """Get the currently playing album."""
        try:
            album = (await self.currentsong())['album']
        except KeyError:
            album = None
        return album

    async def random_album(self, albums):
        """Get a random album from the albums dictionary."""
        albums = list(albums.keys())
        # Everything except the current playing album
        current_album = await self.getcurrent_album()
        if current_album:
            albums.pop(albums.index(current_album))
        if albums:
            return random.choice(albums)
        else:
            return None

    async def play_album(self, album):
        """Play the first song in the given album."""
        song = album[0]
        print('Playing album "%s - %s".' % (song.get('artist', '<no artist>'), song.get('album', '<no album>')))
        await self.playid(song['id'])

    def get_mpd_lib_version(self):
        version = VERSION
        return version[0]*100 + version[1]*10 + version[2]

    async def play_random(self, lib=False, clear=False, base=None):
        """Play a random album from the list of albums."""
        if not lib:  # Play from the playlist
            albums = await self.getalbums()
            toplay = await self.random_album(albums)
            if toplay:  # Make sure we found a random album
                await self.play_album(albums[toplay])
            else:
                print("Nothing to play.")
        else:  # Play from the library
            if clear:
                self.clear()
            album_name = None
            if base:
                album_name = random.choice(await self.list('album', 'base', base))
            else:
                album_name = random.choice(await self.list('album'))

            if self.get_mpd_lib_version() >= 110:
                # Since version 1.1.0 list returns a list of dictionaries
                album_name = album_name['album']
            if album_name:
                if album_name not in await self.getalbums():  # Queue the album if not queued
                    await self.findadd('album', album_name)

                album = (await self.getalbums())[album_name]
                await self.play_album(album)

    def stdio_monitor_thread(self, loop, queue):
        while True:
            sys.stdin.readline()
            # add the message to the queue, don't use queue.put_nowait directly here because the queue
            # itself is not thread safe.
            loop.call_soon_threadsafe(queue.put_nowait, "received line on stdin")

    async def idle_monitor_task(self, queue):
        while True:
            if await self.currentsong():
                async for subsystem in self.idle(["player"]):
                    break
            else:
                await queue.put("current album finished")
                # make sure that the message was handled
                await queue.join()

    async def idleloop(self, lib, clear, base):
        """Loop for daemon mode."""

        # Create a queue that we will use to return events in those two cases:
        # 1. When the player becomes idle.
        # 2. When we received a line on stdin.
        queue = asyncio.Queue(1)

        # Create a task to detect when the player becomes idle.
        idle = asyncio.create_task(self.idle_monitor_task(queue))

        # Create a separate thread that will read from stdin. This is needed because asyncio
        # doesn't support file IO. Don't use the asyncio style "loop.run_in_executor" here
        # because then it wouldn't be possible to stop the process with ctrl-c.
        # See also: https://stackoverflow.com/questions/49992329/the-workers-in-threadpoolexecutor-is-not-really-daemon
        # By using a normal thread we can mark it as a daemon so it will be closed once the main thread exits.
        loop = asyncio.get_running_loop()
        thread = Thread(target=self.stdio_monitor_thread, args=[loop, queue], daemon=True)
        thread.start()

        # both of the above will push messages into the queue
        while True:
            await queue.get()
            await self.play_random(lib, clear, base)
            queue.task_done()

    async def move_album(self, album, pos=0):
        """Insert an album in the playlist."""
        for song in album:
            await self.moveid(song['id'], pos)
            pos += 1

    async def shuffle_albums(self):
        """Shuffle the albums in the playlist."""
        albums = await self.getalbums()

        # Shuffle the albums
        album_names = list(albums.keys())
        random.shuffle(album_names)

        # Insert the new shuffled list
        for album in album_names:
            await self.move_album(albums[album])

async def async_main():
    # Arguments
    arguments = ArgumentParser(description="Pick and play a random album from "
                               "the current playlist")
    arguments.add_argument('-d', '--daemon', action='store_true', dest='daemon',
                    help='run the script in daemon mode.', default=False)
    arguments.add_argument('-l', '--library', action='store_true', dest='library',
                          default=False, help='use the whole library instead of playlist.')
    arguments.add_argument('-c', '--clear', action='store_true', dest='clear',
                          default=False, help='clear the playlist before adding new album when using the whole library')
    arguments.add_argument('-z', '--shuffle', dest="shuffle", action='store_true',
                    default=False, help='shuffle the albums in the current playlist.')
    arguments.add_argument('-p', '--port', dest='port', default=PORT,
                    help='specify mpd\'s port (defaults to {})'.format(PORT), metavar='PORT')
    arguments.add_argument('-u', '--host', dest='host', default=HOST,
                    help='specify mpd\'s host (defaults to {})'.format(HOST), metavar='HOST')
    arguments.add_argument('--password', dest='password', default=PASSWORD,
                           help='specify mpd\'s password', metavar='PASSWORD')
    arguments.add_argument('-b', '--base', dest='base', default=None,
                           help='specify base directory for adding from library')
    args = arguments.parse_args()

    client = Client(args.password)
    await client.connect(args.host, args.port)
    if args.daemon:
        print("Going into daemon mode, press Ctrl-C to exit.")
        print("Press Enter to skip the current album.")
        await client.idleloop(lib=args.library, clear=args.clear, base=args.base)
    elif args.shuffle:
        await client.shuffle_albums()
    else:
        await client.play_random(lib=args.library, clear=args.clear, base=args.base)

def main():
    try:
        asyncio.run(async_main())
    except KeyboardInterrupt:
        raise SystemExit  # No need for the ugly traceback when interrupting.

if __name__ == '__main__':
    main()

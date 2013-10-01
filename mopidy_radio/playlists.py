from __future__ import unicode_literals

import logging

from mopidy.backends import base, listener
from mopidy.models import Playlist, Track

logger = logging.getLogger('mopidy.backends.radio')


class RadioPlaylistsProvider(base.BasePlaylistsProvider):

    def create(self, name):
        pass  # TODO

    def delete(self, uri):
        pass  # TODO

    def lookup(self, uri):
        for playlist in self.playlists:
            if playlist.uri == uri:
                return playlist

    def refresh(self):
        playlists = []
        for favorite in self.backend.config['radio']['favorites']:
            for station in self.backend.session.search_stations_by_string(favorite, 5):
                if station['name'] == favorite:
                    uri = 'radio://' + str(station['id'])
                    tracks = [Track(
                        uri = uri,
                        name = favorite,
                        bitrate = station['bitrate'])]
                    playlist = Playlist(uri = uri,
                                        name = favorite,
                                        tracks = tracks)
                    playlists.append(playlist)
                    break
            else:
                logger.warning('Favorite radio station \'%s\' not found', favorite)
                

        self.playlists = playlists
        listener.BackendListener.send('playlists_loaded')

    def save(self, playlist):
        pass  # TODO
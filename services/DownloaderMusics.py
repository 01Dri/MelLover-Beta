import os
import shutil

import discord
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from pytube import YouTube
from pytube import Search
from constants.Contants import DEFAULT_PATH, CLIENT_SPOTIFY_ID, CLIENT_SECRET_SPOTIFY__ID
from entities.Track import Track


class DownloadMusics:



    def __init__(self, url, ctx):
        self.url = url
        self.ctx = ctx
        pass

    def download_music_for_youtube(self):
        track_api_pytube = YouTube(self.url)
        self.track_entity = Track(track_api_pytube.title, track_api_pytube.length, self.url, self.ctx.author,
                                  self.ctx.author.display_avatar)
        audio_stream = YouTube(self.track_entity.url).streams.filter(only_audio=True).first()
        audio_stream.download(self.get_folder_musics(self.ctx))
        audio_source = discord.FFmpegPCMAudio(os.path.join(self.get_folder_musics(self.ctx), audio_stream.default_filename))
        return audio_source

    def download_music_for_spotify(self, url):
        client_id = CLIENT_SPOTIFY_ID
        client_secret = CLIENT_SECRET_SPOTIFY__ID
        track_info = self.get_dados_for_track_spotify(url)
        audio_stream = track_info[0].streams.filter(only_audio=True).first()
        audio_stream.download(self.get_folder_musics(self.ctx))
        audio_source = discord.FFmpegPCMAudio(
            os.path.join(self.get_folder_musics(self.ctx), audio_stream.default_filename))
        return audio_source


    def get_dados_for_track_spotify(self, url):
        client_id = CLIENT_SPOTIFY_ID
        client_secret = CLIENT_SECRET_SPOTIFY__ID
        auth_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
        sp = spotipy.Spotify(auth_manager=auth_manager)

        track_id = url.split('/')[-1].split('?')[0]
        print(track_id)
        track_info = sp.track(track_id)

        name_track = track_info['name']
        name_artist = track_info['album']['artists'][0]['name']

        url_for_search = name_track + " " + name_artist
        search = Search(url_for_search)
        track = search.results[0]

        return [track, track.title, track.length, url]

    def get_folder_musics(self, ctx):
        folder_for_musics = f"{self.ctx.guild.id}"
        folder_for_musics_path = os.path.join(DEFAULT_PATH, folder_for_musics)
        return folder_for_musics_path

    async def remove_mp4_files(self, ctx):
        shutil.rmtree(self.get_folder_musics(ctx))

    def get_name_track(self):
        print(self.url)



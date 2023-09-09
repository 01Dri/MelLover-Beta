import os
import shutil

import discord
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from pytube import YouTube

from constants.Contants import DEFAULT_PATH, CLIENT_SPOTIFY_ID, CLIENT_SECRET_SPOTIFY__ID
from entities.Track import Track


class DownloadMusics:



    def __init__(self, url, ctx):
        self.url = url
        self.ctx = ctx
        pass

    async def download_music_for_youtube(self):
        print(self.url)
        track_api_pytube = YouTube(self.url)
        self.track_entity = Track(track_api_pytube.title, track_api_pytube.length, self.url, self.ctx.author,
                                  self.ctx.author.display_avatar)
        audio_stream = YouTube(self.track_entity.url).streams.filter(only_audio=True).first()
        audio_stream.download(await self.get_folder_musics(self.ctx))
        print(audio_stream.default_filename)
        audio_source = discord.FFmpegPCMAudio(os.path.join(await self.get_folder_musics(self.ctx), audio_stream.default_filename))
        return audio_source

    def download_music_for_spotify(self):
        client_id = CLIENT_SPOTIFY_ID
        client_secret = CLIENT_SECRET_SPOTIFY__ID
        auth_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
        sp = spotipy.Spotify(auth_manager=auth_manager)

        url = "https://open.spotify.com/intl-pt/track/3nfj9Fdbl30TvcZE9sU0Vx?si=d0edb3154db14a18"

        track_id = url.split('/')[-1].split('?')[0]
        track_info = sp.track(track_id)

        print("Nome da faixa:", track_info['name'])
        print("Artista(s):", ', '.join([artist['name'] for artist in track_info['artists']]))
        print("Álbum:", track_info['album']['name'])




    async def get_folder_musics(self, ctx):
        folder_for_musics = f"{self.ctx.guild.id}"
        folder_for_musics_path = os.path.join(DEFAULT_PATH, folder_for_musics)
        return folder_for_musics_path

    async def remove_mp4_files(self, ctx):
        shutil.rmtree(await self.get_folder_musics(ctx))

    def get_name_track(self):
        print(self.url)


classe = DownloadMusics(None, None)
classe.download_music_for_spotify()





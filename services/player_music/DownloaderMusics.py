import asyncio
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

    def __init__(self):
        pass

    def download_music_for_youtube(self, url, ctx):
        track_api_pytube = YouTube(url)
        track_entity = Track(track_api_pytube.title, track_api_pytube.length, url, ctx.author,
                             ctx.author.display_avatar)

        audio_stream = YouTube(track_entity.url).streams.filter(only_audio=True).first()
        audio_stream.download(self.get_folder_musics(ctx))
        audio_source = discord.FFmpegPCMAudio(
            os.path.join(self.get_folder_musics(ctx), audio_stream.default_filename))
        return audio_source

    def download_music_for_spotify(self, url, ctx):
        client_id = CLIENT_SPOTIFY_ID
        client_secret = CLIENT_SECRET_SPOTIFY__ID
        track_info = self.get_dados_for_track_spotify(url)
        audio_stream = track_info[0].streams.filter(only_audio=True).first()
        audio_stream.download(self.get_folder_musics(ctx))
        audio_source = discord.FFmpegPCMAudio(
            os.path.join(self.get_folder_musics(ctx), audio_stream.default_filename))
        return audio_source

    def get_dados_for_track_spotify(self, url):
        client_id = CLIENT_SPOTIFY_ID
        client_secret = CLIENT_SECRET_SPOTIFY__ID
        auth_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
        sp = spotipy.Spotify(auth_manager=auth_manager)

        track_id = url.split('/')[-1].split('?')[0]
        track_info = sp.track(track_id)

        name_track = track_info['name']
        name_artist = track_info['album']['artists'][0]['name']

        url_for_search = name_track + " " + name_artist
        print(url_for_search)

        search = Search(url_for_search)
        track = search.results[0]
        if not "-" in track.title:
            return [track, name_artist + " - " + track.title, track.length, url]
        else:
            return [track, track.title, track.length, url]

    def get_folder_musics(self, ctx):
        folder_for_musics = f"{ctx.guild.id}"
        folder_for_musics_path = os.path.join(DEFAULT_PATH, folder_for_musics)
        return folder_for_musics_path

    async def remove_mp4_files(self, ctx):
        await asyncio.sleep(5)
        shutil.rmtree(self.get_folder_musics(ctx))

    def get_name_track(self, url):
        print(url)

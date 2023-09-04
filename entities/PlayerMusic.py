import asyncio
import os
import shutil

import discord
from pytube import Playlist
from pytube import YouTube
from entities.Track import Track


class PlayerMusic():
    def __init__(self, ctx):

        self.track = None
        self.ctx = ctx
        self.playlist_queue_pytube = []
        self.playlist_songs = []
        self.pause_status = False
        self.already_playing = False
        self.skip_status = False
        self.voice_channel = ctx.author.voice.channel
        self.voice_client = None
        self.PATH = "C:\\Users\\didvg\\Desktop\\MelLoverOOP\\app"
        self.i = 0

    def load_songs(self, ctx):
        parts = ctx.content.split()
        url = parts[1]
        if "playlist" in url:
            self.playlist_queue_pytube = Playlist(url)
            for track in self.playlist_queue_pytube:
                self.playlist_songs.append(track)
        else:
            self.playlist_songs.append(url)

    def download_music(self, ctx, url):
        track_api_pytube = YouTube(url)
        self.track = Track(track_api_pytube.title, track_api_pytube.length, url, ctx.author, ctx.author.display_avatar)
        audio_stream = YouTube(self.track.url).streams.filter(only_audio=True).first()
        audio_stream.download(self.get_folder_musics(ctx))
        audio_source = discord.FFmpegPCMAudio(f'{self.get_folder_musics(ctx)}/{self.track.name}.mp4')
        return audio_source

    async def play_music(self, ctx):
        try:
            self.voice_client = await self.voice_channel.connect()
            self.load_songs(ctx)
        except Exception as e:
            print(e)
            self.load_songs(ctx)

        while self.playlist_songs:
            await self.verify_status()
            try:
                if not self.skip_status:
                    print(self.playlist_songs)
                    print(f"Musica atual: {self.playlist_songs[self.i]}")
                    self.voice_client.play(self.download_music(ctx, self.playlist_songs[self.i]))
                    self.i += 1
                else:
                    self.skip_status = False
            except Exception as e:
                print(e)
                await asyncio.sleep(180)
                break
        await self.disconnect_for_away(ctx)

    def pause(self):
        self.voice_client.pause()
        self.pause_status = True

    def resume(self):
        self.voice_client.resume()
        self.pause_status = False

    def skip(self):
        self.voice_client.stop()
        self.skip_status = True

    async def stop(self, ctx):
        await self.disconnect(ctx)
        self.pause_status = False
        self.already_playing = False

    async def verify_status(self):
        while self.pause_status or self.voice_client.is_playing():
            await asyncio.sleep(1)

        self.pause_status = False
        self.already_playing = False
        return False

    async def disconnect_for_away(self, ctx):
        if not self.voice_client.is_playing():
            await asyncio.sleep(180)
            await self.disconnect(ctx)

        self.pause_status = False
        self.already_playing = False
        return False

    async def disconnect(self, ctx):
        self.voice_client.stop()
        await self.voice_client.disconnect()
        self.playlist_songs.clear()
        self.i = 0
        self.pause_status = False
        await asyncio.sleep(2)
        self.remove_mp4_files(ctx)

    def remove_mp4_files(self, ctx):
        shutil.rmtree(self.get_folder_musics(ctx))

    def get_folder_musics(self, ctx):
        folder_for_musics = f"{ctx.guild.id}"
        folder_for_musics_path = os.path.join(self.PATH, folder_for_musics)
        return folder_for_musics_path

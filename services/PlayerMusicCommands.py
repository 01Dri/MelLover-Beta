import asyncio
import os
import shutil
import discord

from pytube import Playlist
from pytube import YouTube

from constants.Contants import DEFAULT_PATH
from entities.Track import Track
from entities.PlaylistEntity import PlaylistEntity


class PlayerMusic:
    def __init__(self, ctx):

        self.track_entity = None
        self.track_by_pytube = None
        self.playlist_entity = None
        self.ctx = ctx
        self.playlist_queue_pytube = None
        self.playlist_songs = []
        self.pause_status = False
        self.already_playing = False
        self.skip_status = False
        self.voice_channel = ctx.author.voice.channel
        self.voice_client = None
        self.PATH = DEFAULT_PATH
        self.i = 0
        self.embed_playlist = None
        self.playlist_status = False
        self.music_unit_status = False

    def load_songs(self, ctx):
        parts = ctx.content.split()
        url = parts[1]
        if "playlist" in url:
            self.playlist_queue_pytube = Playlist(url)
            self.music_unit_status = False
            self.playlist_status = True
            try:
                playlist_desc = self.playlist_queue_pytube.description
            except:
                playlist_desc = "Sem descrição"

            self.playlist_entity = PlaylistEntity(self.playlist_queue_pytube.title,
                                                  self.playlist_queue_pytube.length,
                                                  "teste", "teste", playlist_desc)
            for track in self.playlist_queue_pytube:
                self.playlist_songs.append(track)
        else:
            self.playlist_status = False
            self.music_unit_status = True
            self.track_by_pytube = YouTube(url)
            self.track_entity = Track(self.track_by_pytube.title, self.track_by_pytube.length,
                                      1, ctx.author, ctx.author.display_avatar)
            self.playlist_songs.append(url)

    async def download_music(self, ctx, url):
        track_api_pytube = YouTube(url)
        self.track_entity = Track(track_api_pytube.title, track_api_pytube.length, url, ctx.author,
                                  ctx.author.display_avatar)
        audio_stream = YouTube(self.track_entity.url).streams.filter(only_audio=True).first()
        await asyncio.sleep(5)
        print(self.get_folder_musics(ctx))
        audio_stream.download(self.get_folder_musics(ctx))
        print(audio_stream.default_filename)
        audio_source = discord.FFmpegPCMAudio(os.path.join(self.get_folder_musics(ctx), audio_stream.default_filename),
                                              options='-vn -f wav -acodec pcm_s16le -ar 44100 -ac 2')
        return audio_source

    async def play_music(self, ctx):
        await self.connect_bot_and_load_songs(ctx)
        await self.verify_how_to_use_embed(ctx)
        while self.playlist_songs:
            await self.verify_status()
            try:
                if not self.skip_status:
                    print(self.playlist_songs)
                    self.voice_client.play(await self.download_music(ctx, self.playlist_songs[self.i]))
                    await asyncio.sleep(2)
                    await ctx.channel.send(embed=self.track_entity.get_embed_for_track_current())
                    self.i += 1
                else:
                    self.skip_status = False

            except discord.DiscordException as e:
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

    async def verify_how_to_use_embed(self, ctx):
        if self.playlist_status:
            await ctx.channel.send(embed=self.playlist_entity.get_embed_response())
        elif self.music_unit_status:
            await ctx.channel.send(embed=self.track_entity.get_embed_for_track())

    async def connect_bot_and_load_songs(self, ctx):
        try:
            self.voice_client = await self.voice_channel.connect()
            self.load_songs(ctx)
        except discord.DiscordException:
            self.load_songs(ctx)


import discord
from app.entities.Track import Track
from pytube import YouTube
import asyncio
import os
from dotenv import load_dotenv


class PlayerMusic():
    load_dotenv()

    def __init__(self)-> None:

        self.track = None
        self.track_youtube = None
        self.voice_channel = None
        self.voice_client = None
        self.url = None
        self.tracks = []
        self.pause_status = False
        self.count = 0

    async def play_music(self, message):
        voice_client = await self.verify_voice_connect(message)
        if voice_client:
            self.add_track_in_queue(message)
            self.verify_amount_music_in_queue()
            await self.download_and_play_music(message, voice_client)
        else:
            self.add_track_in_queue(message)
            self.verify_amount_music_in_queue()

    async def verify_voice_connect(self, message):
        try:
            voice_channel = message.author.voice.channel
            return await voice_channel.connect()
        except:
            return None

    def get_server_id(self, message):
        return message.guild.id

    def verify_amount_music_in_queue(self):
        print("Lista de faixas na fila:")
        for index, track in enumerate(self.tracks, start=1):
            print(f"{index}. {track.name}")
        print(f"Total de faixas na fila: {len(self.tracks)}")

    def add_track_in_queue(self, message):
        parts_message = message.content.split()
        url_message = parts_message[1]
        track_for_pytube_api = YouTube(url_message)
        self.track = Track(track_for_pytube_api.title, track_for_pytube_api.length, url_message)
        self.tracks.append(self.track)

    async def download_and_play_music(self, message, voice_client):
        while self.tracks:

            audio_stream = YouTube(self.track.url).streams.filter(only_audio=True).first()
            id_server = self.get_server_id(message)
            audio_stream.download(filename=f'{id_server}.mp4')
            source = f'{id_server}.mp4'
            play_source = discord.FFmpegPCMAudio(f'{source}')
            voice_client.play(play_source)
            self.count += 1
            while voice_client.is_playing() or self.pause_status:
                await asyncio.sleep(1)
            if self.count == len(self.tracks):
                break

        await asyncio.sleep(120)
        await voice_client.disconnect()
        await asyncio.sleep(10)
        server_id = self.get_server_id(message)
        os.remove(f'{server_id}.mp4')

    async def pause_music(self, voice_client):
        self.pause_status = True
        if self.pause_status:
            await voice_client.pause()

    async def resume_music(self, voice_client):
        self.pause_status = False
        await voice_client.resume()



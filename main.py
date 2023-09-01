import os
from typing import Any
import discord
from discord.flags import Intents
from discord.ext.commands import Command
from app.entities.PlayerMusic import PlayerMusic

class DiscordBot(discord.Client):

    def __init__(self, *, intents: Intents, **options: Any) -> None:
        self.servers = {}

        super().__init__(intents=intents, **options)

    intents = discord.Intents.default()
    intents.message_content = True
    client = discord.Client(intents=intents)
    @client.event
    async def on_ready(self):
        print(f'Logged on as {self.user}')

    @client.event
    async def on_message(self, message):
        author_voice_state = message.author.voice
        voice_client = author_voice_state.channel.guild.voice_client
        if message.author == self.client.user:
            return
        if message.content.startswith("!play"):
            guild_id = message.guild.id
            if guild_id not in self.servers:
                self.servers[guild_id] = PlayerMusic()
            server = self.servers[guild_id]
            await server.play_music(message)

        if message.content.startswith("!pause"):
            guild_id = message.guild.id
            if guild_id not in self.servers:
                self.servers[guild_id] = PlayerMusic()
            server = self.servers[guild_id]
            await server.pause_music(voice_client)

        if message.content.startswith("!resume"):
            guild_id = message.guild.id
            if guild_id not in self.servers:
                self.servers[guild_id] = PlayerMusic()
            server = self.servers[guild_id]
            await server.resume_music(voice_client)




intents = discord.Intents.default()
intents.message_content = True
client = DiscordBot(intents=intents)
client.run(os.getenv("TOKEN_DISCORD"))

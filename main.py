import os
from typing import Any
import discord
from discord.app_commands import tree
from discord.flags import Intents
from entities.PlayerMusic import PlayerMusic
from dotenv import load_dotenv
from discord import app_commands



class DiscordBot(discord.Client):

    def __init__(self, *, intents: Intents, **options: Any) -> None:
        self.servers = {}
        self.intents = discord.Intents.default()
        self.intents.message_content = True
        self.client = discord.Client(intents=intents)
        super().__init__(intents=intents, **options)

    intents = discord.Intents.default()
    intents.message_content = True
    client = discord.Client(intents=intents)
    tree = app_commands.CommandTree(client)

    @client.event
    async def on_ready(self):
        print(f'Logged on as {self.user}')

    @client.event
    async def on_message(self, message):
        if message.author == self.client.user:
            return

        if message.content.startswith("!play"):
            guild_id = message.guild.id
            if guild_id not in self.servers:
                self.servers[guild_id] = PlayerMusic(message)
            server = self.servers[guild_id]
            await server.play_music(message)

        if message.content.startswith("!pause"):
            guild_id = message.guild.id
            if guild_id not in self.servers:
                self.servers[guild_id] = PlayerMusic(message)
            server = self.servers[guild_id]
            server.pause()

        if message.content.startswith("!resume"):
            guild_id = message.guild.id
            if guild_id not in self.servers:
                self.servers[guild_id] = PlayerMusic(message)
            server = self.servers[guild_id]
            server.resume()

        if message.content.startswith("!stop"):
            guild_id = message.guild.id
            if guild_id not in self.servers:
                self.servers[guild_id] = PlayerMusic(message)
            server = self.servers[guild_id]
            await server.stop(message)

        if message.content.startswith("!skip"):
            guild_id = message.guild.id
            if guild_id not in self.servers:
                self.servers[guild_id] = PlayerMusic(message)
            server = self.servers[guild_id]
            server.skip()


load_dotenv()
intents = discord.Intents.default()
intents.message_content = True
client = DiscordBot(intents=intents)
client.run(os.getenv("TOKEN_DISCORD"))

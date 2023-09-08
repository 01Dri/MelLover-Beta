import os
from typing import Any
import discord
from discord.flags import Intents
from services.PlayerMusicCommands import PlayerMusic
from services.LolServicesCommands import LolServices
from dotenv import load_dotenv
from discord import app_commands


class DiscordBot(discord.Client):

    def __init__(self, *, intents: Intents, **options: Any) -> None:
        self.intents = discord.Intents.default()
        self.intents.message_content = True
        self.client = discord.Client(intents=intents)
        self.guid_musicas = {}
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
        global player
        if message.author == self.client.user:
            return

        if isinstance(message.channel, discord.TextChannel):
            if message.guild.id not in self.guid_musicas:
                self.guid_musicas[message.guild.id] = PlayerMusic(message.guild.id)

        if message.content.startswith("!play"):
            await self.guid_musicas[message.guild.id].play_music(message)

        if message.content.startswith("!pause"):
            await self.guid_musicas[message.guild.id].pause(message)

        if message.content.startswith("!resume"):
            await self.guid_musicas[message.guild.id].resume(message)

        if message.content.startswith("!skip"):
            await self.guid_musicas[message.guild.id].skip(message)

        if message.content.startswith("!stop"):
            await self.guid_musicas[message.guild.id].stop(message)

        if message.content.startswith("!contalol"):
            user_lol_services = LolServices(message)
            await user_lol_services.get_view_account_for_nick(message)


load_dotenv()
intents = discord.Intents.default()
intents.message_content = True
client = DiscordBot(intents=intents)
client.run(os.getenv("TOKEN_DISCORD"))

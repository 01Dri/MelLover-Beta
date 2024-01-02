import time

from services.league_of_legends_account.LolServices import LolServices
from services.player_music.PlayerMusicCommands import PlayerMusic


class BotCommands:

    def __init__(self, client) -> None:
        self.client = client
        self.guid_musics = {}  # This is for each user to have their own instance of PlayerMusic by

    async def handler_commands(self, ctx):
        if ctx.author == self.client.user:
            return
        content_message = ctx.content.lower()
        if content_message.startswith("!contalol"):
            lol_services = LolServices(ctx)
            inicio = time.time()
            await lol_services.get_account_lol_info(ctx)
            fim = time.time()
            tempo_execucao = fim - inicio
            print(f"A função levou {tempo_execucao} segundos para executar.")

        if ctx.content.startswith("!m"):
            if ctx.guild.id not in self.guid_musicas:
                self.guid_musics[ctx.guild.id] = PlayerMusic(ctx.guild.id)

            if ctx.content.startswith("!mplay"):
                await self.guid_musics[ctx.guild.id].play_music(ctx)

            if ctx.content.startswith("!mpause"):
                await self.guid_musics[ctx.guild.id].pause(ctx)

            if ctx.content.startswith("!mresume"):
                await self.guid_musics[ctx.guild.id].resume(ctx)

            if ctx.content.startswith("!mskip"):
                await self.guid_musics[ctx.guild.id].skip(ctx)

            if ctx.content.startswith("!mstop"):
                await self.guid_musics[ctx.guild.id].stop(ctx)

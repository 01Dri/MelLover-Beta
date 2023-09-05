import discord
from pytube import YouTube


class EmbedsCustom:

    def __init__(self):
        pass

    def create_embed_add_music_queue(self, url, author, playlist_queue):
        embed = discord.Embed(title="Mel Musicas")
        video = YouTube(url)
        embed.add_field(name="Música adicionada na fila: ", value=video.title)
        embed.add_field(name="Posição na fila: ", value=playlist_queue.index(url) + 1)
        embed.set_footer(text=f'Pedida por {author}', icon_url=author.display_avatar)
        return embed

    def create_embed_for_playlist_music(self, title, length, description):
        embed = discord.Embed(title="Mel Musicas", color=0x87CEFA)
        embed.add_field(name=f"Playlist", value=f"{title.upper()}")
        embed.add_field(name=f"Descrição: ", value=f"{description}", inline=False)
        embed.add_field(name=f"Músicas: ", value=f"{length} músicas carregadas", inline=False)
        return embed


    def create_embed_for_music_unit(self, track, min, seg, author):
        embed = discord.Embed(title="Mel Musicas", color=0x87CEFA)
        embed.add_field(name="Música atual: ", value=f"{track.title}", inline=True)
        embed.add_field(name="Tempo de duração", value=f"{min}:{seg:02d} minutos.", inline=True)
        embed.add_field(name="Posição na fila:", value=f"{self.i + 1}", inline=True)
        embed.set_footer(text=f'Pedida por {author}', icon_url=author.display_avatar)
        embed.set_image(url=track.thumbnail_url)

        return embed
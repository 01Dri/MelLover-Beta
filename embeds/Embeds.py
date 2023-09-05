import discord


def create_embed_for_playlist_music(title, length, description):
    embed = discord.Embed(title="Mel Musicas", color=0x87CEFA)
    embed.add_field(name=f"Playlist", value=f"{title.upper()}")
    embed.add_field(name=f"Descrição: ", value=f"{description}", inline=False)
    embed.add_field(name=f"Músicas: ", value=f"{length} músicas carregadas", inline=False)
    return embed


def create_embed_for_music_unit(track, author):
    embed = discord.Embed(title="Mel Musicas", color=0x87CEFA)
    embed.add_field(name="Música adicionada: ", value=f"{track}", inline=True)
    embed.set_footer(text=f'Pedida por {author}', icon_url=author.display_avatar)
    return embed


def create_embed_for_music_current(track, author):
    embed = discord.Embed(title="Mel Musicas", color=0x87CEFA)
    embed.add_field(name="Música atual: ", value=f"{track}", inline=False)
    embed.set_footer(text=f'Pedida por {author}', icon_url=author.display_avatar)
    return embed


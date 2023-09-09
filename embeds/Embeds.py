import discord

from constants.Contants import COLOR_FOR_EMBEDS
from constants.Contants import COLOR_FOR_EMBEDS_ERROR

def create_embed_for_playlist_music(title, length, description):
    embed = discord.Embed(title="Mel Musicas", color=COLOR_FOR_EMBEDS)
    embed.add_field(name=f"Playlist", value=f"{title.upper()}")
    embed.add_field(name=f"Descrição: ", value=f"{description}", inline=False)
    embed.add_field(name=f"Músicas: ", value=f"{length} músicas carregadas", inline=False)
    return embed


def create_embed_for_music_unit(track, author):
    embed = discord.Embed(title="Mel Musicas", color=COLOR_FOR_EMBEDS)
    embed.add_field(name="Música adicionada: ", value=f"{track}", inline=True)
    embed.set_footer(text=f'Pedida por {author}', icon_url=author.display_avatar)
    return embed


def create_embed_for_music_current(track, author):
    embed = discord.Embed(title="Mel Musicas", color=COLOR_FOR_EMBEDS)
    embed.add_field(name="Música atual: ", value=f"{track}", inline=False)
    embed.set_footer(text=f'Pedida por {author}', icon_url=author.display_avatar)
    return embed

def create_embed_for_account_league(nick, league, tier, level, winrate,pdl, op_gg, url_splash_art_champ):
    embed = discord \
        .Embed(
        title='League of legends Account', description="Info account", color=COLOR_FOR_EMBEDS)
    embed.add_field(name="NICKNAME", value=nick.upper(), inline=False)
    embed.add_field(name="ELO", value=tier + " " + league, inline=False)
    embed.add_field(name="LEVEL", value=level, inline=False)
    embed.add_field(name="WINRATE", value=f'{winrate}%', inline=False)
    embed.add_field(name="PDL", value=pdl, inline=False)
    embed.add_field(name="OPGG", value=op_gg, inline=False)
    embed.set_image(url=url_splash_art_champ)
    return embed


def create_embed_for_error_link_music():
    embed = discord.Embed(title="Mel Musicas", color=COLOR_FOR_EMBEDS_ERROR)
    embed.add_field(name="ERRO: ", value="Link informado é inválido!", inline=False)
    return embed

def create_embed_for_error_voice_connect():
    embed = discord.Embed(title="Mel Musicas", color=COLOR_FOR_EMBEDS_ERROR)
    embed.add_field(name="ERRO: ", value="**Você precisa estar conectado em um canal de voz para usar esse comando!**", inline=False)
    return embed

def create_embed_for_skip(next_music):
    embed = discord.Embed(title="Mel Musicas", color=COLOR_FOR_EMBEDS)
    embed.add_field(name=f"Próxima na fila é: **{next_music}**", value=f"", inline=False)
    return embed

def create_embed_for_pause():
    embed = discord.Embed(title="Mel Musicas", color=COLOR_FOR_EMBEDS)
    embed.add_field(name=f"Músicas pausada!", value=f"", inline=True)
    return embed

def create_embed_for_resume():
    embed = discord.Embed(title="Mel Musicas", color=COLOR_FOR_EMBEDS)
    embed.add_field(name=f"Música retomada!", value=f"", inline=True)
    return embed

def create_embed_for_stop():
    embed = discord.Embed(title="Mel Musicas", color=COLOR_FOR_EMBEDS)
    embed.add_field(name=f"Até a próxima!!!", value="", inline=True)
    return embed


def create_embed_for_error_account_invalid_league(nick):
    embed = discord.Embed(title="League of legends Account", color=COLOR_FOR_EMBEDS_ERROR)
    embed.add_field(name="ERRO: ", value=f'Nick **{nick}** não existe no sistema.', inline=False)
    return embed



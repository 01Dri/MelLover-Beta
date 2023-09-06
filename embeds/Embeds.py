import discord

from constants.Contants import COLOR_FOR_EMBEDS


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

def create_embed_for_account_league(nick, league, tier, level, winrate,pdl, op_gg):
    embed = discord \
        .Embed(
        title='League of legends Account', description="Info account", color=COLOR_FOR_EMBEDS)
    embed.add_field(name="NICKNAME", value=nick.upper(), inline=False)
    embed.add_field(name="ELO", value=tier + " " + league, inline=False)
    embed.add_field(name="LEVEL", value=level, inline=False)
    embed.add_field(name="WINRATE", value=f'{winrate}%', inline=False)
    embed.add_field(name="PDL", value=pdl, inline=False)
    embed.add_field(name="OPGG", value=op_gg, inline=False)
    embed.set_image(url="https://files.tecnoblog.net/wp-content/uploads/2019/05/league-of-legends-700x394.jpg")
    return embed

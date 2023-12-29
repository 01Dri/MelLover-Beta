import urllib.parse
from entities.DiscordAccount import DiscordAccount
from exceptions.league_of_legends_exceptions.FailedGetSummonerByNick import FailedGetSummonerByNick
from services.extenal_api.ApiRiotLol import ApiRiot
from constants.Contants import TOKEN_RIOT
from exceptions.league_of_legends_exceptions.NickIsNone import NickIsNone
from embeds.Embeds import ViewEmbedLol


class LolServices:

    def __init__(self, ctx):
        self.account_discord = DiscordAccount(ctx.author)
        self.lol_api_services = ApiRiot(TOKEN_RIOT)
        self.view_embeds = ViewEmbedLol()

    async def get_entity_account_lol(self, ctx):
        global nick
        try:
            nick = self.parser_nick_command(ctx)
            entity_account = self.lol_api_services.get_entity_account_lol(nick)
            await self.view_embeds.get_embed_account_lol(ctx, entity_account.nick, entity_account.league,
                                                         entity_account.tier, entity_account.level,
                                                         entity_account.winrate, entity_account.pdl,
                                                         entity_account.op_gg, entity_account.best_champ)
        except NickIsNone:
            await self.view_embeds.get_embed_account_lol_nick_is_none(ctx)
        except FailedGetSummonerByNick:
            await self.view_embeds.get_embed_account_lol_nick_not_exist(ctx, nick)

    def parser_nick_command(self, ctx):
        parts = ctx.content.split()
        global nick
        if len(parts) > 1 and parts[0] == "!contalol":
            nick = urllib.parse.quote(" ".join(parts[1:]))
            return nick
        raise NickIsNone("Nick doesn't can be none")

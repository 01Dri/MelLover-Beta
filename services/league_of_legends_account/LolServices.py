import urllib.parse
from entities.entities_discord_account.DiscordAccount import DiscordAccount
from exceptions.league_of_legends_exceptions.FailedGetSummonerByNick import FailedGetSummonerByNick
from exceptions.league_of_legends_exceptions.SummonerAccountNotHaveInfoSoloDuoQueue import \
    SummonerAccountNotHaveInfoSoloDuoQueue
from services.league_of_legends_account.external_api.ApiRiotLol import ApiRiot
from constants.Contants import TOKEN_RIOT
from exceptions.league_of_legends_exceptions.NickIsNone import NickIsNone
from view.view_league_of_legends.ViewEmbedLol import ViewEmbedLol


class LolServices:

    def __init__(self, ctx):
        self.account_discord = DiscordAccount(ctx.author)
        self.lol_api_services = None
        self.view_embeds = ViewEmbedLol()
        self.nick = None

    async def get_account_lol_info(self, ctx):
        self.lol_api_services = ApiRiot(self.nick, TOKEN_RIOT)
        try:
            self.nick = self.parser_nick_command(ctx)
            self.lol_api_services = ApiRiot(self.nick, TOKEN_RIOT)
            entity_account = self.lol_api_services.get_entity_account_lol()
            await self.view_embeds.get_embed_account_lol(ctx, entity_account.nick, entity_account.league,
                                                         entity_account.tier, entity_account.level,
                                                         entity_account.winrate, entity_account.pdl,
                                                         entity_account.op_gg, entity_account.best_champ)
        except NickIsNone:
            await self.view_embeds.get_embed_account_lol_nick_is_none(ctx)
        except FailedGetSummonerByNick:
            await self.view_embeds.get_embed_account_lol_nick_not_exist(ctx, self.nick)
        except SummonerAccountNotHaveInfoSoloDuoQueue:
            await self.view_embeds.get_embed_account_lol_without_solo_duo_info(ctx, self.nick, self.lol_api_services.get_level_account_by_nick(), f"https://www.op.gg/summoners/br/{self.nick}")

    def parser_nick_command(self, ctx):
        parts = ctx.content.split()
        if len(parts) > 1 and parts[0] == "!contalol":
            self.nick = urllib.parse.quote(" ".join(parts[1:]))
            return self.nick
        raise NickIsNone("Nick doesn't can be none")

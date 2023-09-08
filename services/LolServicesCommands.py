import urllib.parse
from entities.AccountLoL import AccountLoL
from entities.DiscordAccount import DiscordAccount
from services.ApiLolServices import get_account_league
from embeds.Embeds import create_embed_for_error_account_invalid_league


class LolServices:

    def __init__(self, ctx):
        self.info_account_league = None
        self.nick = None
        self.tier = None
        self.league = None
        self.level = None
        self.winrate = None
        self.pdl = 0
        self.nick_in_game = None
        self.op_gg_account = None
        self.account_lol = None
        self.account_discord = DiscordAccount(ctx.author)
        pass

    async def get_view_account_for_nick(self, ctx):
        parts = ctx.content.split()
        if len(parts) > 1 and parts[0] == "!contalol":
            self.nick = urllib.parse.quote(" ".join(parts[1:]))
        try:
            await self.get_account_league_info(ctx)
            if self.nick != " " or self.nick is not None:
                self.account_lol = AccountLoL(self.nick_in_game, self.level, self.league, self.tier, self.winrate,
                                              self.pdl, self.op_gg_account, self.account_discord)
                await ctx.reply(embed=self.account_lol.get_embed_for_account_league())
        except:
            print("conta inválida")

    async def get_account_league_info(self, ctx):
        try:
            info_account_league = get_account_league(self.nick)
            self.nick_in_game = info_account_league[0]
            self.tier = info_account_league[1]
            self.league = info_account_league[2]
            self.level = info_account_league[3]
            self.winrate = info_account_league[4]
            self.pdl = info_account_league[5]
            self.op_gg_account = info_account_league[6]
        except:
            await ctx.reply(embed=create_embed_for_error_account_invalid_league(self.nick))

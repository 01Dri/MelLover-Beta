import urllib.parse
from entities.AccountLoL import AccountLoL
from entities.DiscordAccount import DiscordAccount
from services.ApiLolServices import get_account_league


class LolServices:

    def __init__(self, ctx):
        self.info_account_league = None
        self.nick = None
        self.tier = None
        self.league = None
        self.level = None
        self.winrate = None
        self.nick_in_game = None
        self.op_gg_account = None
        self.account_lol = None
        self.account_discord = DiscordAccount(ctx.author)
        pass

    async def get_view_account_for_nick(self, ctx):
        parts = ctx.content.split()
        if len(parts) > 1 and parts[0] == "!contalol":
            self.nick = urllib.parse.quote(" ".join(parts[1:]))
        self.get_account_league_info()
        if self.nick != " " or self.nick is not None:
            self.account_lol = AccountLoL(self.nick_in_game, self.level, self.league, self.tier, self.winrate, self.op_gg_account, self.account_discord)
            await ctx.reply(embed=self.account_lol.get_embed_for_account_league())


    def get_account_league_info(self):
        info_account_league = get_account_league(self.nick)
        self.nick_in_game = info_account_league[0]
        self.tier = info_account_league[1]
        self.league = info_account_league[2]
        self.level = info_account_league[3]
        self.winrate = info_account_league[4]
        self.op_gg_account = info_account_league[5]

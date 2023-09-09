from embeds.Embeds import create_embed_for_account_league


class AccountLoL:

    def __init__(self, nick, level, league, tier, winrate, pdl, op_gg, discord_account, name_champ_for_splash):
        self.nick = nick
        self.leve = level
        self.league = league
        self.tier = tier
        self.winrate = winrate
        self.pdl = pdl
        self.op_gg = op_gg
        self.discord_account = discord_account
        self.name_champ_for_splash = name_champ_for_splash
        pass

    def get_embed_for_account_league(self):
        return create_embed_for_account_league(self.nick, self.league, self.tier, self.leve, self.winrate, self.pdl, self.op_gg, self.name_champ_for_splash)



import requests
from exceptions.league_of_legends_exceptions.ErrorGetValueHashMapInfoAccount import ErrorGetValueHashMapInfoAccount
from exceptions.league_of_legends_exceptions.FailedGetSummonerByNick import FailedGetSummonerByNick
from exceptions.league_of_legends_exceptions.FailedGetInfoLeagueByUserId import FailedGetInfoLeagueByUserId
from exceptions.league_of_legends_exceptions.FailedGetSummonerLevel import FailedGetSummonerLevel
from exceptions.league_of_legends_exceptions.FailedGetWinrateSummonerByNick import FailedGetWinrateSummonerByNick
from exceptions.league_of_legends_exceptions.FailedGetIdChampMaestryByNick import FailedGetIdChampMaestryByNick
from exceptions.league_of_legends_exceptions.FailedGetNameChampById import FailedGetNameChampById
from exceptions.league_of_legends_exceptions.RiotTokenInvalid import RiotTokenInvalid
from entities.entities_league_of_legends_account.AccountLoL import AccountLoL
from exceptions.league_of_legends_exceptions.SummonerAccountNotHaveInfoSoloDuoQueue import \
    SummonerAccountNotHaveInfoSoloDuoQueue
from logger.LoggerConfig import LoggerConfig


class ApiRiot:

    def __init__(self, nick, token) -> None:
        self.token = token
        self.headers_token = {
            'X-Riot-Token': f'{self.token}'
        }
        self.logger = LoggerConfig()
        self.nick = nick
        self.puuid = None
        self.rank = None
        self.tier = None
        self.pdl = None
        self.level = None
        self.winrate = None
        self.id_best_champion = None
        self.nick_name_best_champ = None
        self.url_splash_art_best_champ = None
        self.id_account = self.get_account_id_by_nick()

    def validation_token(self, response):
        self.logger.get_logger_info_level().info("VALIDATING TOKEN BY RESPONSE STATUS CODE")
        if response.status_code == 403 or response.status_code == 401:
            response_json = response.json()
            status = response_json['status']
            message = status['message']
            self.logger.get_logger_info_error().error("TOKEN INVALID ERROR TRIGGERED")
            raise RiotTokenInvalid(
                f"Failed to sent request because the token is invalid, status code: {response.status_code} and message error: {message}")

    def get_entity_account_lol(self):
        info_account_hash_map = self.get_all_info_account_league()
        try:
            id_account = info_account_hash_map['id']
            nick = info_account_hash_map['nick']
            level = info_account_hash_map['level']
            rank = info_account_hash_map['rank']
            tier = info_account_hash_map['tier']
            winrate = info_account_hash_map['winrate']
            pdl = info_account_hash_map['pdl']
            op_gg = info_account_hash_map['op_gg']
            best_champ_url = info_account_hash_map['best_champ']
            account_lol_entity = AccountLoL(id_account, nick, level, rank, tier, winrate, pdl, op_gg, best_champ_url)
            return account_lol_entity
        except KeyError as e:
            self.logger.get_logger_info_error().error(
                "ERROR ON FUNCTION 'GET_ENTITY_ACCOUNT_LOL' GET VALUES OF HASH MAP")
            raise ErrorGetValueHashMapInfoAccount(f"ERROR WHILE GET VALUES OF HASH MAP WITH INFO ACCOUNT LEAGUE: {e}")

    def get_all_info_account_league(self):
        self.get_account_id_by_nick()
        self.get_account_tier_rank_and_pdl()
        op_gg_account = f"https://www.op.gg/summoners/br/{self.nick}"
        self.get_level_account_by_nick()
        self.get_winrate_account_by_nick()
        hash_map_info = {'id': self.id_account, 'nick': self.nick, 'tier': self.tier, 'rank': self.rank,
                         'pdl': self.pdl, 'level': self.level, 'winrate': self.winrate,
                         'op_gg': op_gg_account, 'best_champ': self.get_url_splash_art_best_champ_by_id_champ()}
        return hash_map_info

    def get_account_id_by_nick(self):
        endpoint_get_summoner_by_nick_riot = f'https://br1.api.riotgames.com/lol/summoner/v4/summoners/by-name/{self.nick}'
        response_api = requests.get(endpoint_get_summoner_by_nick_riot, headers=self.headers_token)
        self.validation_token(response_api)
        if response_api.status_code != 200 and response_api.status_code != 403 and response_api.status_code != 401:
            raise FailedGetSummonerByNick(
                f'Failed to recover summoners info by nick, status code: {response_api.status_code}')
        response_api_json = response_api.json()
        self.id_account = response_api_json['id']
        self.puuid = response_api_json['puuid'] # ID ALTERNATIVE RIOT ACCOUNT
        return self.id_account

    def get_account_tier_rank_and_pdl(self):
        endpoint_get_summoner_league_by_id_riot = f"https://br1.api.riotgames.com/lol/league/v4/entries/by-summoner/{self.id_account}"
        response_api = requests.get(endpoint_get_summoner_league_by_id_riot, headers=self.headers_token)
        self.validation_token(response_api)
        if response_api.status_code != 200 and response_api.status_code != 403 and response_api.status_code != 401:
            raise FailedGetInfoLeagueByUserId(
                f'Failed to recover league info by id, status code: {response_api.status_code}')
        response_api_json = response_api.json()
        for item in response_api_json:
            if item.get('queueType') == 'RANKED_SOLO_5x5':
                self.tier = item.get('tier')
                self.rank = item.get('rank')
                self.pdl = item.get('leaguePoints')
                break
        else:
            raise SummonerAccountNotHaveInfoSoloDuoQueue("Summoner not have a solo queue info")

    def get_level_account_by_nick(self):
        endpoint_get_level_league_by_id_riot = f'https://br1.api.riotgames.com/lol/summoner/v4/summoners/by-name/{self.nick}'
        response_api = requests.get(endpoint_get_level_league_by_id_riot, headers=self.headers_token)
        self.validation_token(response_api)
        if response_api.status_code != 200 and response_api.status_code != 403 and response_api.status_code != 401:
            raise FailedGetSummonerLevel(f'Failed to get summoner level. status code: {response_api.status_code}')
        response_api_json = response_api.json()
        self.level = response_api_json['summonerLevel']
        return self.level

    def get_winrate_account_by_nick(self):
        API_ENDPOINT_RIOT_LEAGUE = f'https://br1.api.riotgames.com/lol/league/v4/entries/by-summoner/{self.id_account}'
        response_api = requests.get(API_ENDPOINT_RIOT_LEAGUE, headers=self.headers_token)
        self.validation_token(response_api)
        if response_api.status_code != 200 and response_api.status_code != 403 and response_api.status_code != 401:
            raise FailedGetWinrateSummonerByNick(
                f'Failed to get winrate summoner, status code: {response_api.status_code}')
        response_api_json = response_api.json()
        wins = 0
        losses = 0
        for item in response_api_json:
            if item.get("queueType") == "RANKED_SOLO_5x5":
                wins = item.get("wins")
                losses = item.get("losses")
                break
        if wins == 0 and losses == 0:
            return 0
        total_games = wins + losses
        winrate = (wins / total_games) * 100
        winrate_round = round(winrate)
        self.winrate = winrate_round
        return self.winrate

    # --- THESE FUNCTIONS BELLOW DON'T WORK ON MOMENT --- #
    def get_id_best_champion_account_by_puuid(self):
        endpoint_get_id_champ_riot = f"https://br1.api.riotgames.com/lol/champion-mastery/v4/champion-masteries/by-puuid/{self.puuid}" ## By Summoner Id was deprecated  now it needs PUUID
        response_api = requests.get(endpoint_get_id_champ_riot, headers=self.headers_token)
        self.validation_token(response_api)
        if response_api.status_code != 200 and response_api.status_code != 403 and response_api.status_code != 401:
            raise FailedGetIdChampMaestryByNick(f'Failed to get id champ, status code: {response_api.status_code}')
        response_api_json = response_api.json()
        champ_max_maestry = max(response_api_json, key=lambda x: x['championPoints'])
        id_champ_max = champ_max_maestry['championId']
        self.id_best_champion = id_champ_max
        return id_champ_max

    def get_name_by_champion_id(self):
        endpoint_dragon_league_of_legends = "http://ddragon.leagueoflegends.com/cdn/13.17.1/data/en_US/champion.json"
        response_api = requests.get(endpoint_dragon_league_of_legends)
        if response_api.status_code != 200 and response_api.status_code != 403 and response_api.status_code and 401:
            raise FailedGetNameChampById(f"Failed to get name champ by id, status code: {response_api.status_code}")
        data = response_api.json()
        champions = data["data"]
        champion = next((champ for champ in champions.values() if champ["key"] == str(self.id_best_champion)), None)
        champion_name = champion["name"]
        self.nick_name_best_champ = champion_name
        return champion_name

    def get_url_splash_art_best_champ_by_id_champ(self):
        self.get_id_best_champion_account_by_puuid()
        self.get_name_by_champion_id()
        url_image_champ_splash = f"http://ddragon.leagueoflegends.com/cdn/img/champion/splash/{self.nick_name_best_champ}_0.jpg"
        self.url_splash_art_best_champ = url_image_champ_splash
        return url_image_champ_splash

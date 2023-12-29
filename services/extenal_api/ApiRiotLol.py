import requests
from exceptions.league_of_legends_exceptions.FailedGetSummonerByNick import FailedGetSummonerByNick
from exceptions.league_of_legends_exceptions.FailedGetInfoLeagueByUserId import FailedGetInfoLeagueByUserId
from exceptions.league_of_legends_exceptions.FailedGetSummonerLevel import FailedGetSummonerLevel
from exceptions.league_of_legends_exceptions.FailedGetWinrateSummonerByNick import FailedGetWinrateSummonerByNick
from exceptions.league_of_legends_exceptions.FailedGetIdChampMaestryByNick import FailedGetIdChampMaestryByNick
from exceptions.league_of_legends_exceptions.FailedGetNameChampById import FailedGetNameChampById
from exceptions.league_of_legends_exceptions.RiotTokenInvalid import RiotTokenInvalid
from entities.AccountLoL import AccountLoL


class ApiRiot:

    def __init__(self, token) -> None:
        self.token = token
        self.headers_token = {
            'X-Riot-Token': f'{self.token}'
        }

    def validation_token(self, response):
        if response.status_code == 403 or response.status_code == 401:
            response_json = response.json()
            status = response_json['status']
            message = status['message']
            raise RiotTokenInvalid(
                f"Failed to sent request because the token is invalid, status code: {response.status_code} and message error: {message}")

    def get_entity_account_lol(self, nick):
        info_account_hash_map = self.parser_info_json_to_hash_map(nick)
        id = info_account_hash_map['id']
        nick = info_account_hash_map['nick']
        level = info_account_hash_map['level']
        rank = info_account_hash_map['rank']
        tier = info_account_hash_map['tier']
        winrate = info_account_hash_map['winrate']
        pdl = info_account_hash_map['pdl']
        op_gg = info_account_hash_map['op_gg']
        best_champ_url = info_account_hash_map['best_champ']
        account_lol_entity = AccountLoL(id, nick, level, rank, tier, winrate, pdl, op_gg, best_champ_url)
        return account_lol_entity

    def get_account_id_by_nick(self, nick):
        endpoint_get_summoner_by_nick_riot = f'https://br1.api.riotgames.com/lol/summoner/v4/summoners/by-name/{nick}'
        response_api = requests.get(endpoint_get_summoner_by_nick_riot, headers=self.headers_token)
        self.validation_token(response_api)
        if response_api.status_code != 200 and response_api.status_code != 403 and response_api.status_code != 401:
            raise FailedGetSummonerByNick(
                f'Failed to recover summoners info by nick, status code: {response_api.status_code}')
        response_api_json = response_api.json()
        return response_api_json['id']

    def get_account_all_info(self, nick):
        id_account_user = self.get_account_id_by_nick(nick)
        endpoint_get_summoner_league_by_id_riot = f"https://br1.api.riotgames.com/lol/league/v4/entries/by-summoner/{id_account_user}"
        response_api = requests.get(endpoint_get_summoner_league_by_id_riot, headers=self.headers_token)
        self.validation_token(response_api)
        if response_api.status_code != 200 and response_api.status_code != 403 and response_api.status_code != 401:
            raise FailedGetInfoLeagueByUserId(
                f'Failed to recover league info by id, status code: {response_api.status_code}')
        return response_api.json()

    def parser_info_json_to_hash_map(self, nick):
        json_account_info = self.get_account_all_info(nick)
        id_account = self.get_account_id_by_nick(nick)
        op_gg_account = f"https://www.op.gg/summoners/br/{nick}"
        level = self.get_level_account(nick)
        # best_champ_url = self.get_url_image_for_champ_max_maestry(nick)
        winrate_account = self.get_winrate_account_by_nick(nick)
        hash_map_info = {}
        for item in json_account_info:
            if item.get('queueType') == 'RANKED_SOLO_5x5':
                hash_map_info['id'] = id_account
                hash_map_info['nick'] = nick
                hash_map_info['tier'] = item.get('tier')
                hash_map_info['rank'] = item.get('rank')
                hash_map_info['pdl'] = item.get('leaguePoints')
                hash_map_info['level'] = level
                hash_map_info['winrate'] = winrate_account
                hash_map_info['op_gg'] = op_gg_account
                hash_map_info['best_champ'] = "yasuo"
        return hash_map_info

    def get_level_account(self, nick):
        endpoint_get_level_league_by_id_riot = f'https://br1.api.riotgames.com/lol/summoner/v4/summoners/by-name/{nick}'
        response_api = requests.get(endpoint_get_level_league_by_id_riot, headers=self.headers_token)
        self.validation_token(response_api)
        if response_api.status_code != 200 and response_api.status_code != 403 and response_api.status_code != 401:
            raise FailedGetSummonerLevel(f'Failed to get summoner level. status code: {response_api.status_code}')
        response_api_json = response_api.json()
        level = response_api_json['summonerLevel']
        return level

    def get_winrate_account_by_nick(self, nick):
        id_account = self.get_account_id_by_nick(nick)
        API_ENDPOINT_RIOT_LEAGUE = f'https://br1.api.riotgames.com/lol/league/v4/entries/by-summoner/{id_account}'
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
        total_games = wins + losses
        winrate = (wins / total_games) * 100
        winrate_round = round(winrate)
        return winrate_round


    # --- THESE FUNCTIONS BELLOW DON'T WORK ON MOMENT --- #
    def get_id_champ_maestry_by_nick_summoner(self, nick):
        id_summoner = self.get_account_id_by_nick(nick)
        endpoint_get_id_champ_riot = f"https://br1.api.riotgames.com/lol/champion-mastery/v4/champion-masteries/by-summoner/{id_summoner}"
        response_api = requests.get(endpoint_get_id_champ_riot, self.headers_token)
        self.validation_token(response_api)
        if response_api.status_code != 200 and response_api.status_code != 403 and response_api.status_code != 401:
            raise FailedGetIdChampMaestryByNick(f'Failed to get id champ, status code: {response_api.status_code}')
        response_api_json = response_api.json()
        champ_max_maestry = max(response_api_json, key=lambda x: x['championPoints'])
        id_champ_max = champ_max_maestry['championId']
        return id_champ_max

    def get_name_by_champion_id(self, nick):
        endpoint_dragon_league_of_legends = "http://ddragon.leagueoflegends.com/cdn/13.17.1/data/en_US/champion.json"
        id_champ = self.get_id_champ_maestry_by_nick_summoner(nick)
        response_api = requests.get(endpoint_dragon_league_of_legends)
        if response_api.status_code != 200 and response_api.status_code != 403 and response_api.status_code and 401:
            raise FailedGetNameChampById(f"Failed to get name champ by id, status code: {response_api.status_code}")
        data = response_api.json()
        champions = data["data"]
        champion = next((champ for champ in champions.values() if champ["key"] == str(id_champ)), None)
        champion_name = champion["name"]
        return champion_name

    def get_url_image_for_champ_max_maestry(self, nick):
        nickname_for_champ = self.get_name_by_champion_id(nick)
        url_image_champ_splash = f"http://ddragon.leagueoflegends.com/cdn/img/champion/splash/{nickname_for_champ}_0.jpg"
        return url_image_champ_splash


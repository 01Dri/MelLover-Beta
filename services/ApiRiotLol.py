import requests
from exceptions import FailedGetSummonerByNick, FailedGetInfoLeagueByUserId, FailedGetSummonerLevel, FailedGetWinrateSummonerByNick, FailedGetIdChampMaestryByNick, FailedGetNameChampById
from entities import AccountLoL

class ApiRiot:

    def __init__(self, token) -> None:
        self.token = token
        self.headers_token = {
            'Authorization': f'Bearer {self.token}'
        }
        pass
    def get_account_id_by_nick(self, nick):
        endpoint_get_summoner_by_nick_riot = f'https://br1.api.riotgames.com/lol/summoner/v4/summoners/by-name/{nick}'
        response_api = requests.get(endpoint_get_summoner_by_nick_riot, headers=self.headers_token)
        if response_api.status_code != 200:
            raise FailedGetSummonerByNick(f'Failed to recover summoners info by nick, status code: {response_api.status_code}')
        response_api_json = response_api.json()
        return response_api_json['id']

    def get_account_all_info(self, nick):
        id_account_user = self.get_account_id_by_nick(nick)
        endpoint_get_summoner_league_by_id_riot = f"https://br1.api.riotgames.com/lol/league/v4/entries/by-summoner/{id_account_user}"
        response_api = requests.get(endpoint_get_summoner_league_by_id_riot, headers=self.headers_token)
        if response_api.status_code != 200:
            raise FailedGetInfoLeagueByUserId(f"Failed to recover league info by id, status code: {response_api.status_code})
        return  response_api.json()

    def parser_info_json_to_hash_map(self, json_account_info, nick, id_account):
        op_gg_account = f"https://www.op.gg/summoners/br/{nick}"
        level = self.get_level_account(id_account)
        best_champ_url = self.get_url_image_for_champ_max_maestry(nick)
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
                hash_map_info['best_champ'] = best_champ_url
        return hash_map_info

    def get_level_account(self, nick):
        endpoint_get_level_league_by_id_riot = f'https://br1.api.riotgames.com/lol/summoner/v4/summoners/by-name/{nick}'
        response_api = requests.get(endpoint_get_level_league_by_id_riot, headers=self.headers_token)
        if response_api.status_code == 200:
            response_api_json = response_api.json()
            level = response_api_json['summonerLevel']
            return level
        raise FailedGetSummonerLevel(f'Failed to get summoner level. status code: {response_api.status_code}')


    def get_entity_account_lol(self, json_account_info, nick, id_account):
        info_account_hash_map = self.parser_info_json_to_hash_map(json_account_info, nick, id_account)
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

    def get_winrate_account_by_nick(self, nick):
        id_account = self.get_account_id_by_nick(nick)
        endpoint_get_winrate_account_riot = f'https://br1.api.riotgames.com/lol/league/v4/entries/by-summoner/{id_account}'
        response_api = requests.get(endpoint_get_winrate_account_riot, self.headers_token)
        if response_api.status_code == 200:
            response_api_json = response_api.json()
            wins = 0
            losses = 0
            for item in response_api_json:
                if item.get('queueType') == 'RANKED_SOLO_5x5':
                    wins = item.get('wins')
                    losses = item.get('losses')
                    break
            total_games = wins + losses
            winrate = (wins / total_games) * 100
            winrate_round = round(winrate)
            return winrate_round
        raise FailedGetWinrateSummonerByNick(f'Failed to get winrate summoner, status code: {response_api.status_code}')



    def get_id_champ_maestry_by_nick_summoner(self, nick):
        id_summoner = self.get_account_id_by_nick(nick)
        endpoint_get_id_champ_riot = f"https://br1.api.riotgames.com/lol/champion-mastery/v4/champion-masteries/by-summoner/{id_summoner}"
        response_api = requests.get(endpoint_get_id_champ_riot, self.headers_token)
        if response_api.status_code == 200:
            response_api_json = response_api.json()
            champ_max_maestry = max(response_api_json, key=lambda x: x['championPoints'])
            id_champ_max = champ_max_maestry['championId']
            return id_champ_max
        raise FailedGetIdChampMaestryByNick(f'Failed to get id champ, status code: {response_api.status_code}')



    def get_name_for_champion_id(self, nick):
        endpoint_dragon_league_of_legends = "http://ddragon.leagueoflegends.com/cdn/13.17.1/data/en_US/champion.json"
        id_champ = self.get_id_champ_maestry_by_nick_summoner(nick)
        response = requests.get(endpoint_dragon_league_of_legends)
        if response.status_code == 200:
            data = response.json()
            champions = data["data"]
            champion = next((champ for champ in champions.values() if champ["key"] == str(id_champ)), None)
            champion_name = champion["name"]
            return champion_name
        raise FailedGetNameChampById(f"Failed to get name champ by id, status code: {response.status_code}")

    def get_url_image_for_champ_max_maestry(self, nick):
        nickname_for_champ = self.get_name_for_champion_id(nick)
        url_image_champ_splash = f"http://ddragon.leagueoflegends.com/cdn/img/champion/splash/{nickname_for_champ}_0.jpg"
        return  url_image_champ_splash



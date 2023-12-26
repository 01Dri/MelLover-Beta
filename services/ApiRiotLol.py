import requests
from exceptions import FailedGetSummonerByNick, FailedGetInfoLeagueByUserId
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
            raise FailedGetSummonerByNick("Failed to recover summoners info by nick, status code: ", response_api.status_code)
        response_api_json = response_api.json()
        return response_api_json['id']
    
    def get_account_all_info(self, nick):
        id_account_user = self.get_account_id_by_nick(nick)
        endpoint_get_summoner_league_by_id_riot = f"https://br1.api.riotgames.com/lol/league/v4/entries/by-summoner/{id_account_user}"
        response_api = requests.get(endpoint_get_summoner_league_by_id_riot, headers=self.headers_token)
        if response_api.status_code != 200:
            raise FailedGetInfoLeagueByUserId("Failed to recover league info by id, status code: ", response_api.status_code)
        response_api_json = response_api.json()
        account_lol_user =  AccountLoL()

    def parser_info_json_to_hash_map(self, json_account_info, nick, id_account):
        op_gg_account = f"https://www.op.gg/summoners/br/{nick}"
        level = self.get_level_account(id_account)
        winrate_account = 0 # I need to adjust this after
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
        return hash_map_info

    def get_level_account(self, id_account_user):
        endpoint_get_level_league_by_id_riot = f'https://br1.api.riotgames.com/lol/summoner/v4/summoners/by-name/{nick}?api_key={TOKEN_RIOT}'
        response_api = requests.get(endpoint_get_level_league_by_id_riot, headers=self.headers_token)
        response_api_json = response_api.json()
        level = response_api_json['summonerLevel']
        return level

    def get_entity_account_lol(self, json_account_info, nick, id_account):
        info_account_hash_map = self.parser_info_json_to_hash_map(json_account_info, nick, id_account)
        nick =
        level =
        rank =
        tier =
        winrate =
        pdl =
        op_gg =
        best_champ =
        account_lol_entity = AccountLoL()

def get_level_account(nick):
    api_account_informations = f'https://br1.api.riotgames.com/lol/summoner/v4/summoners/by-name/{nick}?api_key={TOKEN_RIOT}'
    response_api = requests.get(api_account_informations)
    response_api_json = response_api.json()
    level = response_api_json['summonerLevel']
    return level

def get_winrate_account_league(nick):
    wins = 0
    losses = 0
    id_league = get_account_id_league(nick)
    if id_league is False:
        return False
    else:
        api_account_informations = f"https://br1.api.riotgames.com/lol/league/v4/entries/by-summoner/{id_league}?api_key={TOKEN_RIOT}"
        response_api = requests.get(api_account_informations)
        response_api_json = response_api.json()
        try:
            for item in response_api_json:
                if item.get('queueType') == 'RANKED_SOLO_5x5':
                    wins = item.get('wins')
                    losses = item.get('losses')
                    break
            total_games = wins + losses
            winrate = (wins / total_games) * 100
            winrate_round = round(winrate)
            return winrate_round
        except:
            return 0

def get_id_champ_maestry_for_nick_sumonner(nick):
    id_summoner = get_account_id_league(nick)
    api_riot = f"https://br1.api.riotgames.com/lol/champion-mastery/v4/champion-masteries/by-summoner/{id_summoner}?api_key={TOKEN_RIOT}"
    response_api = requests.get(api_riot)
    response_api_json = response_api.json()
    champ_max_maestry = max(response_api_json, key=lambda x: x['championPoints'])
    id_champ_max = champ_max_maestry['championId']
    return id_champ_max


        
def get_name_for_champion_id(nick):
    url = "http://ddragon.leagueoflegends.com/cdn/13.17.1/data/en_US/champion.json"
    id_champ = get_id_champ_maestry_for_nick_sumonner(nick)
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        champions = data["data"]

        champion = next((champ for champ in champions.values() if champ["key"] == str(id_champ)), None)
        champion_name = champion["name"]
        return champion_name


def get_url_image_for_champ_max_maestry(nick):
    nickname_for_champ = get_name_for_champion_id(nick)
    api_splash = f"http://ddragon.leagueoflegends.com/cdn/img/champion/splash/{nickname_for_champ}_0.jpg"
    return  api_splash



import requests
from constants.Contants import TOKEN_RIOT

def get_account_id_league(nick):

    api_account_informations = f'https://br1.api.riotgames.com/lol/summoner/v4/summoners/by-name/{nick }?api_key={TOKEN_RIOT}'
    response_api = requests.get(api_account_informations)
    if response_api.status_code != 200:
        return False
    else:
        response_api_json = response_api.json()
        return response_api_json['id']

def get_account_league(nick):
    tier = ""
    league = ""
    level = ""
    pdl = 0
    op_gg_account = f"https://www.op.gg/summoners/br/{nick}"
    winrate = 0
    id_league = get_account_id_league(nick)
    if id_league is False:
        return False
    else:

        api_elo_info = f"https://br1.api.riotgames.com/lol/league/v4/entries/by-summoner/{get_account_id_league(nick)}?api_key={TOKEN_RIOT}"
        response_api = requests.get(api_elo_info)
        response_api_json = response_api.json()
        try:
            for item in response_api_json:
                if item.get('queueType') == 'RANKED_SOLO_5x5':
                    tier = item.get('tier')
                    league = item.get('rank')
                    pdl = item.get('leaguePoints')
                    break

            nick_in_game = response_api_json[0]['summonerName']
            level = get_level_account(nick)
            winrate = get_winrate_account_league(nick)
            account = [nick_in_game, tier, league,level, winrate, pdl, op_gg_account]
            return account

        except:
            level = get_level_account(nick)
            dados = [nick, "", "Sem elo", level, winrate, 0, op_gg_account]
            return dados

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



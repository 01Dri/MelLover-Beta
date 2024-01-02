import unittest

from constants.Contants import TOKEN_RIOT
from exceptions.league_of_legends_exceptions.FailedGetSummonerByNick import FailedGetSummonerByNick
from exceptions.league_of_legends_exceptions.RiotTokenInvalid import RiotTokenInvalid
from exceptions.league_of_legends_exceptions.SummonerAccountNotHaveInfoSoloDuoQueue import \
    SummonerAccountNotHaveInfoSoloDuoQueue
from services.league_of_legends_account.external_api.ApiRiotLol import ApiRiot


class ApiRioIntegrationTests(unittest.TestCase):
    def test_get_account_entity(self):
        api_riot_lol = ApiRiot("Drikill", TOKEN_RIOT)
        entity_result = api_riot_lol.get_entity_account_lol()
        self.assertEqual("Drikill", entity_result.nick)
        self.assertEqual(402, entity_result.level)
        self.assertEqual("PLATINUM", entity_result.tier)
        self.assertEqual(51, entity_result.winrate)
        self.assertEqual(0, entity_result.pdl)

    def test_get_id_account_by_nick(self):
        api_riot_lol = ApiRiot("Drikill", TOKEN_RIOT)
        id_account_result = api_riot_lol.get_account_id_by_nick()
        self.assertEqual("VDOzqowJuT3rRD76FfHfuckdsVUIfC7ST70PZB9JVi-51X4",
                         id_account_result)

    def test_level_account(self):
        api_riot_lol = ApiRiot("Drikill", TOKEN_RIOT)
        level_result = api_riot_lol.get_level_account_by_nick()
        self.assertEqual(402, level_result)

    def test_get_winrate_account_by_nick(self):
        api_riot_lol = ApiRiot("Drikill", TOKEN_RIOT)
        result_winrate = api_riot_lol.get_winrate_account_by_nick()
        self.assertEqual(51, result_winrate)

    def test_get_account_without_win_and_losses_winrate_by_nick(self):
        api_riot_lol = ApiRiot("Drikill", TOKEN_RIOT)
        result_winrate = api_riot_lol.get_winrate_account_by_nick()
        self.assertEqual(51, result_winrate)

    def test_get_all_account_info(self):
        api_riot_lol = ApiRiot("Drikill", TOKEN_RIOT)
        json_result = api_riot_lol.get_account_all_info()
        global tier
        for item in json_result:
            if item.get('queueType') == 'RANKED_SOLO_5x5':
                tier = item.get('tier')
        self.assertEqual("PLATINUM", tier)

    def test_get_all_account_info2(self):
        api_riot_lol = ApiRiot("Raposy", TOKEN_RIOT)
        json_result = api_riot_lol.get_account_all_info()
        global tier
        for item in json_result:
            if item.get('queueType') == 'RANKED_SOLO_5x5':
                tier = item.get('tier')
        self.assertEqual("PLATINUM", tier)

    def test_get_all_account_info3(self):
        api_riot_lol = ApiRiot("130722", TOKEN_RIOT)
        json_result = api_riot_lol.get_account_all_info()
        global tier
        for item in json_result:
            if item.get('queueType') == 'RANKED_SOLO_5x5':
                tier = item.get('tier')
        self.assertEqual("GOLD", tier)

    def test_exception_account_without_info_solo_queue_account(self):
        api_riot_lol = ApiRiot("Dri", TOKEN_RIOT)  # Account Dri not have a info on soloqueue
        with self.assertRaises(SummonerAccountNotHaveInfoSoloDuoQueue) as context:
            api_riot_lol.parser_info_json_to_hash_map()
        self.assertEqual(str(context.exception),
                         "Summoner not have a solo queue info")  # 404 data not found

    ## Missing test get_id_champ, get_name_champ and get_entity_account

    def test_exception_invalid_token_request(self):
        with self.assertRaises(RiotTokenInvalid):
            ApiRiot("Drikill", "token_errado")

    def test_exception_failed_get_summoner_id_by_nick(self):
        with self.assertRaises(FailedGetSummonerByNick) as context:
            ApiRiot("Duvido esse nick existir", TOKEN_RIOT)
        self.assertEqual(str(context.exception),
                         "Failed to recover summoners info by nick, status code: 404")  # 404 data not found


if __name__ == '__main__':
    unittest.main()

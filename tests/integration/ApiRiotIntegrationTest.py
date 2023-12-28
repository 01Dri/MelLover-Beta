import unittest

from constants.Contants import TOKEN_RIOT
from exceptions.FailedGetSummonerByNick import FailedGetSummonerByNick
from exceptions.FailedGetSummonerLevel import FailedGetSummonerLevel
from services.ApiRiotLol import ApiRiot
from exceptions.RiotTokenInvalid import RiotTokenInvalid


class ApiRioIntegrationTests(unittest.TestCase):
    def test_get_id_account_by_nick(self):
        api_riot_lol = ApiRiot(TOKEN_RIOT)
        id_account_result = api_riot_lol.get_account_id_by_nick("Drikill")
        self.assertEqual("VDOzqowJuT3rRD76FfHfuckdsVUIfC7ST70PZB9JVi-51X4",
                         id_account_result)

    def test_level_account(self):
        api_riot_lol = ApiRiot(TOKEN_RIOT)
        level_result = api_riot_lol.get_level_account("Drikill")
        self.assertEqual(402, level_result)

    def test_get_account_entity(self):  ## Test for last
        api_riot_lol = ApiRiot(TOKEN_RIOT)
        result_entity = api_riot_lol.get_entity_account_lol("Drikill")
        self.assertEqual("Drikill", result_entity.nick)

    def test_get_winrate_account_by_nick(self): # This doesn't working ?????????
        api_riot_lol = ApiRiot(TOKEN_RIOT)
        result_winrate = api_riot_lol.get_winrate_account_by_nick("Drikill")
        self.assertEqual(50, result_winrate)

    def test_exception_invalid_token_request(self):
        api_riot_lol = ApiRiot("token_errado")
        with self.assertRaises(RiotTokenInvalid):
            api_riot_lol.get_account_id_by_nick("Drikill")

    def test_exception_failed_get_summoner_id_by_nick(self):
        api_riot_lol = ApiRiot(TOKEN_RIOT)
        with self.assertRaises(FailedGetSummonerByNick) as context:
            api_riot_lol.get_account_id_by_nick("Duvido esse nick existir")
        self.assertEqual(str(context.exception),
                         "Failed to recover summoners info by nick, status code: 404")  # 404 data not found

    def test_exception_failed_get_level_account_by_nick(self):
        api_riot_lol = ApiRiot(TOKEN_RIOT)
        with self.assertRaises(FailedGetSummonerLevel) as context:
            api_riot_lol.get_level_account("Duvido esse nick existir")
        self.assertEqual(str(context.exception), "Failed to get summoner level. status code: 404")


if __name__ == '__main__':
    unittest.main()

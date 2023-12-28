import unittest

from constants.Contants import TOKEN_RIOT
from exceptions.FailedGetSummonerByNick import FailedGetSummonerByNick
from services.ApiRiotLol import ApiRiot


class ApiRioIntegrationTests(unittest.TestCase):
    def test_get_id_account_by_nick(self):
        api_riot_lol = ApiRiot(TOKEN_RIOT)
        id_account_result = api_riot_lol.get_account_id_by_nick("Drikill")
        self.assertEqual("VDOzqowJuT3rRD76FfHfuckdsVUIfC7ST70PZB9JVi-51X4",
                         id_account_result)

# Improve validations how token and status code
    def test_exception_failed_get_id_summoner_by_nick(self):
        api_riot_lol = ApiRiot("token_errado")
        with self.assertRaises(FailedGetSummonerByNick):
            api_riot_lol.get_account_id_by_nick("Drikill")

if __name__ == '__main__':
    unittest.main()

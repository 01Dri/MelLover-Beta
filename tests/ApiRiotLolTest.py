import unittest
from services.ApiRiotLol import ApiRiot

from constants.Contants import TOKEN_RIOT

class MyTestCase(unittest.TestCase):
    def test_something(self):
        self.assertEqual(True, False)  # add assertion here
    def test_entity_account_lol(self):
        api_riot_lol = ApiRiot(TOKEN_RIOT)
        json = api_riot_lol.get_account_all_info("Drikill")
        entity = api_riot_lol.get_entity_account_lol(json, "Drikill")

if __name__ == '__main__':
    unittest.main()

import unittest

from exceptions.league_of_legends_exceptions.FailedGetSummonerByNick import FailedGetSummonerByNick
from exceptions.league_of_legends_exceptions.RiotTokenInvalid import RiotTokenInvalid
from services.league_of_legends_account.extenal_api.ApiRiotLol import ApiRiot
from constants.Contants import TOKEN_RIOT
from unittest.mock import MagicMock, patch


class ApiRiotTest(unittest.TestCase):
    def test_get_account_id_by_nick(self):
        with patch('requests.get') as mock_get:
            api_riot_lol = ApiRiot(TOKEN_RIOT)
            mock_response = MagicMock()
            mock_response.status_code = 200
            mock_response.json.return_value = {'id': 5}
            mock_get.return_value = mock_response
            id_account_result = api_riot_lol.get_account_id_by_nick("Drikill")
            self.assertEqual(5, id_account_result)

    def test_get_level_account(self):
        with patch('requests.get') as mock_get:
            api_riot_lol = ApiRiot(TOKEN_RIOT)
            mock_response_request = MagicMock()
            mock_response_request.status_code = 200
            mock_response_request.json.return_value = {"summonerLevel": 402}
            mock_get.return_value = mock_response_request
            level_result = api_riot_lol.get_level_account("Drikill")
            self.assertEqual(402, level_result)

    def test_get_winrate_account_by_nick(self):
        with patch('requests.get') as mock_get:
            api_riot_lol = ApiRiot(TOKEN_RIOT)
            mock_response_request = MagicMock()
            mock_response_request.status_code = 200
            mock_response_request.json.return_value = [
                {
                    "queueType": "RANKED_SOLO_5x5",
                    "wins": 5,
                    "losses": 10
                }
            ]
            mock_get.return_value = mock_response_request
            with patch.object(ApiRiot, 'get_account_id_by_nick') as mock_get_account_id:
                mock_get_account_id.return_value = 5
                winrate_result = api_riot_lol.get_winrate_account_by_nick("Drikill")
                self.assertEqual(33, winrate_result)

    ## Missing test get_id_champ, get_name_champ and get_entity_account

    def test_exception_failed_get_id_account(self):
        with patch('requests.get') as mock_get:
            api_riot_lol = ApiRiot(TOKEN_RIOT)
            mock_response = MagicMock()
            mock_response.status_code = 400  # Bad request
            mock_response.json.return_value = {'message': 'Failed get id'}
            mock_get.return_value = mock_response
            with self.assertRaises(FailedGetSummonerByNick) as context:
                api_riot_lol.get_account_id_by_nick("Drikill")
            self.assertEqual(str(context.exception), "Failed to recover summoners info by nick, status code: 400")

    def test_exception_riot_invalid_token(self):
        with patch('requests.get') as mock_get:
            api_riot_lol = ApiRiot(TOKEN_RIOT)
            mock_response = MagicMock()
            mock_response.status_code = 401  # Unauthorized
            mock_response.json.return_value = {
                "status": {
                    "message": "Invalid Token",
                    "status_code": 401
                }
            }
            mock_get.return_value = mock_response
            with self.assertRaises(RiotTokenInvalid) as context:
                api_riot_lol.get_account_id_by_nick("Drikill")
            self.assertEqual(str(context.exception),
                             "Failed to sent request because the token is invalid, status code: 401 and message error: Invalid Token")


if __name__ == '__main__':
    unittest.main()

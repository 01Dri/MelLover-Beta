import unittest

from exceptions.FailedGetSummonerByNick import FailedGetSummonerByNick
from exceptions.RiotTokenInvalid import RiotTokenInvalid
from services.ApiRiotLol import ApiRiot
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



    def test_parser_info_json_to_hash_map(self):  ## Test this after fix get level
        mock_api_riot_lol_mock = MagicMock()
        mock_requests = MagicMock()
        mock_api_riot_lol_mock.get_account_all_info.return_value = {
            "queueType": "RANKED_SOLO_5x5",
            "tier": "3",
            "rank": "GOLD",
            "leaguePoints": 50
        }
        mock_api_riot_lol_mock.get_account_id_by_nick.return_value = 5
        mock_api_riot_lol_mock.get_level_account.return_value = 30  # I need to fix this
        mock_api_riot_lol_mock.get_url_image_for_champ_max_maestry.return_value = 'https://teste.png'
        mock_api_riot_lol_mock.get_winrate_account_by_nick.return_value = 50.0
        api_riot = ApiRiot(TOKEN_RIOT)
        map_result = api_riot.parser_info_json_to_hash_map("Drikill")
        self.assertEqual("5", map_result['id'])

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

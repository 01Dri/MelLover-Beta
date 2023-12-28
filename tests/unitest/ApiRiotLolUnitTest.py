import unittest
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


if __name__ == '__main__':
    unittest.main()

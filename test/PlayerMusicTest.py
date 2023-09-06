import unittest
from services.PlayerMusic import PlayerMusic


class PlayerMusicTest(unittest.TestCase):

    def load_songs(self):

       player = PlayerMusic()
       url = "https://www.youtube.com/watch?v=wz7dSGjiSgY&list=PLPzULCdMTsR-ARB4c5e08PioFwks16APQ&index=1&pp=gAQBiAQB8AUB"
       self.assertEqual(1, len(player.load_songs(url)))


if __name__ == '__main__':
    unittest.main()

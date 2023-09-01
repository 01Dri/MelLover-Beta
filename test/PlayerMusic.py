import unittest
from app.entities.PlayerMusic import PlayerMusic
from app.entities.Track import Track
class MyTestCase(unittest.TestCase):

    def test_play_music_player(self):
        self.track = Track("diego_music", None, None)
        self.player = PlayerMusic()
        self.assertTrue(self.player.play_music(self.track))


if __name__ == '__main__':
    unittest.main()

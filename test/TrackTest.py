import unittest
from app.entities.Track import Track


class TrackTests(unittest.TestCase):

    def test_track_info(self):
        track = Track("diego", 266, "url_musica")
        self.assertIsNotNone(track)
        self.assertEqual("diego", track.name)
        self.assertEqual(266, track.time)
        self.assertEqual("url_musica", track.url)


if __name__ == '__main__':
    unittest.main()

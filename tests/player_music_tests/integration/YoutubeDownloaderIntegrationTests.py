import unittest

from exceptions.player_music_exceptions.UrlInvalidFormatYoutubeException import UrlInvalidFormatYoutubeException
from services.player_music.YoutubeDownloader import YoutubeDownloader


class YoutubeDownloaderTest(unittest.TestCase):

    def test_parse_url_invalid_exception(self):
        url_test = "esse_url_aqui_é_zoado"
        youtube_downloader = YoutubeDownloader(url_test, None)
        with self.assertRaises(UrlInvalidFormatYoutubeException) as context:
            youtube_downloader.parse_url_youtube()
        self.assertEqual("The url must be from YouTube", str(context.exception))

    def test_parse_url(self):
        url_test = "https://www.youtube.com/watch?v=5eDk-kTE9DI"
        youtube_downloader = YoutubeDownloader(url_test, None)
        self.assertTrue(youtube_downloader)
    def test_verify_if_file_music_saved(self):
        url_test = "https://www.youtube.com/watch?v=5eDk-kTE9DI"
        youtube_downloader = YoutubeDownloader(url_test, "C:\\Users\\didvg\\Desktop\\DevFolders\\MelLover2.0folder_for_downloads_musics\\")
        youtube_downloader.download_music().create_entity_track()
        self.assertTrue(youtube_downloader.verify_downloaded_music_file_exist())

if __name__ == '__main__':
    unittest.main()

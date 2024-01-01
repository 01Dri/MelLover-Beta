import asyncio
import unittest

from exceptions.player_music_exceptions.UrlInvalidFormatYoutubeException import UrlInvalidFormatYoutubeException
from services.player_music.YoutubeDownloader import YoutubeDownloader


class YoutubeDownloaderTest(unittest.TestCase):

    def test_one_download_music(self):
        url_test = "https://www.youtube.com/watch?v=5eDk-kTE9DI"
        youtube_downloader = YoutubeDownloader(
            "C:\\Users\\didvg\\Desktop\\DevFolders\\MelLover2.0folder_for_downloads_musics\\")
        youtube_downloader.add_music_queue_download(url_test)
        youtube_downloader.download_music()
        result = youtube_downloader.create_entity_track()
        youtube_downloader.verify_downloaded_music_file_exist(None)
        self.assertEqual("Joji - Nectar (Full Album)", result.title)
        self.assertEqual("FINISH", youtube_downloader.status_download)

    def test_multiple_download_music(self):
        url_test = "https://www.youtube.com/watch?v=5eDk-kTE9DI"
        url_test2 = "https://www.youtube.com/watch?v=ppSWrh9r9Do"
        youtube_downloader = YoutubeDownloader(
            "C:\\Users\\didvg\\Desktop\\DevFolders\\MelLover2.0folder_for_downloads_musics\\")
        youtube_downloader.add_music_queue_download(url_test)
        youtube_downloader.add_music_queue_download(url_test2)
        youtube_downloader.download_music()
        result = youtube_downloader.create_entity_track()
        youtube_downloader.verify_downloaded_music_file_exist(result)
        self.assertEqual("I DONT WANT TO BE WITH YOU", result.title)
        self.assertEqual("FINISH", youtube_downloader.status_download)

    def test_failed_status_download_music(self):
        url_test = "https://www.youtube.com/w"
        youtube_downloader = YoutubeDownloader(
            "C:\\Users\\didvg\\Desktop\\DevFolders\\MelLover2.0folder_for_downloads_musics\\")
        youtube_downloader.add_music_queue_download(url_test)
        youtube_downloader.download_music()
        self.assertEqual("ERROR", youtube_downloader.status_download)

    def test_parse_url_invalid_exception(self):
        url_test = "esse_url_aqui_é_zoado"
        youtube_downloader = YoutubeDownloader(None)
        with self.assertRaises(UrlInvalidFormatYoutubeException) as context:
            youtube_downloader.parse_url_youtube(url_test)
        self.assertEqual("The url must be from YouTube", str(context.exception))

    def test_parse_url(self):
        url_test = "https://www.youtube.com/watch?v=5eDk-kTE9DI"
        youtube_downloader = YoutubeDownloader(None)
        self.assertTrue(youtube_downloader.parse_url_youtube(url_test))

    def test_verify_if_file_music_saved(self):
        url_test = "https://www.youtube.com/watch?v=5eDk-kTE9DI"
        youtube_downloader = YoutubeDownloader("C:\\Users\\didvg\\Desktop\\DevFolders\\MelLover2.0folder_for_downloads_musics\\")
        youtube_downloader.add_music_queue_download(url_test)
        youtube_downloader.download_music()
        track_result = youtube_downloader.create_entity_track()
        self.assertTrue(youtube_downloader.verify_downloaded_music_file_exist(track_result))


if __name__ == '__main__':
    unittest.main()

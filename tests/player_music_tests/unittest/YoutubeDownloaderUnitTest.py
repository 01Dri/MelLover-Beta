import unittest
from unittest.mock import MagicMock, patch

from services.player_music.YoutubeDownloader import YoutubeDownloader
from tests.tools.MockDownloadFile import create_file_test

class YoutubeDownloaderUnitTest(unittest.TestCase):


## FINISH THIS FUNCTION TEST AFTER ##
    def test_download_music(self):
        with patch('pytube.YouTube') as mock_pytube:
            instance = mock_pytube.return_value
            instance.title = "teste.txt"
            audio_stream_pytube = mock_pytube.streams.filter(only_audio=True).first()
            audio_stream_pytube.download.return_value = create_file_test(
                "C:\\Users\\didvg\\Desktop\\DevFolders\\MelLover2.0folder_for_downloads_musics")
            youtube_downloader = YoutubeDownloader("https://www.youtube.com/watch?v=fGn_ikKMdIk",
                                                   "C:\\Users\\didvg\\Desktop\\DevFolders\\MelLover2.0folder_for_downloads_musics")
            result_entity = youtube_downloader.create_entity_track()
            print(result_entity.title)
            self.assertTrue(youtube_downloader.parse_url_youtube().download_music().verify_downloaded_music_file_exist())


if __name__ == '__main__':
    unittest.main()

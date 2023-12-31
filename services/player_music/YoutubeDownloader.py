import os.path

from pytube import YouTube
from entities.player_music.YoutubeTrack import YoutubeTrack
from constants.DownloadStates import DownloadStates
import logging

from exceptions.player_music_exceptions.NotFoundMusicFile import NotFoundMusicFile
from exceptions.player_music_exceptions.UrlInvalidFormatYoutubeException import UrlInvalidFormatYoutubeException


class YoutubeDownloader:

    def __init__(self, url, path):
        self.track_pytube = None
        self.url = url
        self.path = path  # Folder to save downloaded musics
        self.status_download = None
        self.track_entity = None
        self.track_pytube = None

    def parse_url_youtube(self):
        if not self.url.startswith("https://www.youtube.com/"):
            raise UrlInvalidFormatYoutubeException("The url must be from YouTube")
        return self

    def download_music(self):

        logging.info(f"DOWNLOADING MUSIC STATE: {DownloadStates.IN_PROGRESS.name}")
        self.status_download = DownloadStates.IN_PROGRESS
        self.track_pytube = YouTube(self.url)
        print(self.track_pytube)
        audio_stream_pytube = self.track_pytube.streams.filter(only_audio=True).first()  # Getting only audio by youtube
        audio_stream_pytube.download(self.path)
        logging.info(f"DOWNLOADING MUSIC STATE: {DownloadStates.FINISH.name}")
        self.status_download = DownloadStates.FINISH
        return self

    def create_entity_track(self):
        self.track_entity = YoutubeTrack(
            self.track_pytube.title,
            self.url,
            self.track_pytube.length,
            self.track_pytube.author
        )
        return self.track_entity

    def verify_downloaded_music_file_exist(self):
        path_music_name = f'{self.track_entity.title}.mp4'
        print(self.path + path_music_name)
        print(self.path)
        full_path_final = os.path.join(self.path, path_music_name)
        if os.path.exists(full_path_final):
            return True
        raise NotFoundMusicFile("")

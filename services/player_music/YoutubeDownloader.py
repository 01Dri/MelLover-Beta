import asyncio
import os.path

from pytube import YouTube
from pytube.exceptions import RegexMatchError

from entities.player_music.YoutubeTrack import YoutubeTrack
from constants.DownloadStates import DownloadStates
import logging

from exceptions.player_music_exceptions.NotFoundMusicFile import NotFoundMusicFile
from exceptions.player_music_exceptions.NotFoundUrlMusicInQueue import NotFoundMusicUrlInQueue
from exceptions.player_music_exceptions.UrlInvalidFormatYoutubeException import UrlInvalidFormatYoutubeException
from queue import PriorityQueue


class YoutubeDownloader:

    def __init__(self, path):
        self.track_pytube = None
        self.path = path  # Folder to save downloaded musics
        self.status_download = None
        self.track_pytube = None
        self.queue = PriorityQueue()

    def add_music_queue_download(self, url):
        self.parse_url_youtube(url)
        self.queue.put(url)
        return self

    def parse_url_youtube(self, url):
        if not url.startswith("https://www.youtube.com/"):
            raise UrlInvalidFormatYoutubeException("The url must be from YouTube")
        return True

    def get_info_track(self):
        try:
            current_url = self.queue.get()
            self.track_pytube = YouTube(current_url)
            return self.track_pytube
        except RegexMatchError:
            raise UrlInvalidFormatYoutubeException("Invalid format url youtube")

    def download_music(self):
        while int(self.queue.qsize() > 0):
            logging.info(f"DOWNLOADING MUSIC STATE: {DownloadStates.IN_PROGRESS.name}")
            self.status_download = DownloadStates.IN_PROGRESS
            try:
                audio_stream_pytube = self.get_info_track().streams.filter(
                    only_audio=True).first()  # Getting only audio by youtube
                audio_stream_pytube.download(self.path)
                logging.info(f"DOWNLOADING MUSIC STATE: {DownloadStates.FINISH.name}")
                self.status_download = DownloadStates.FINISH.name
            except UrlInvalidFormatYoutubeException:
                self.status_download = DownloadStates.ERROR.name

    def create_entity_track(self):
        track_entity = YoutubeTrack(
            self.track_pytube.title,
            None,
            self.track_pytube.length,
            self.track_pytube.author
        )
        return track_entity

    def verify_downloaded_music_file_exist(self, track_entity):
        print(track_entity)
        if track_entity is None:
            track_entity = self.create_entity_track()
        path_music_name = f'{track_entity.title}.mp4'
        full_path_final = os.path.join(self.path, path_music_name)
        if os.path.exists(full_path_final):
            return True
        raise NotFoundMusicFile("")

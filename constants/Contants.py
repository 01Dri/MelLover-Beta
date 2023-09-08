from  dotenv import load_dotenv
import os

load_dotenv()
DEFAULT_PATH = os.getcwd()
TOKEN_RIOT = os.getenv("TOKEN_RIOT")
COLOR_FOR_EMBEDS = 0x87CEFA
COLOR_FOR_EMBEDS_ERROR = 0xFF0000
LINK_FOR_YOUTUBE = "https://www.youtube.com/"
LINK_MUSIC_UNIT_FOR_YOUTUBE = "https://www.youtube.com/watch"
PLAYLIST_LINK = "https://www.youtube.com/playlist"
from  dotenv import load_dotenv
import os

load_dotenv()
DEFAULT_PATH = os.getcwd()
TOKEN_RIOT = os.getenv("TOKEN_RIOT")
CLIENT_SPOTIFY_ID = os.getenv("TOKEN_CLIENT_ID_SPOTIFY")
CLIENT_SECRET_SPOTIFY__ID = os.getenv("TOKEN_CLIENT_SECRET")

COLOR_FOR_EMBEDS = 0x87CEFA
COLOR_FOR_EMBEDS_ERROR = 0xFF0000
LINK_FOR_YOUTUBE = "https://www.youtube.com/"
LINK_MUSIC_UNIT_FOR_YOUTUBE = "https://www.youtube.com/watch"
PLAYLIST_LINK = "https://www.youtube.com/playlist"
LINK_FOR_SPOTIFY = "https://open.spotify.com/intl-pt/track/"
LINK_FOR_SPOTIFY_MOBAL = " https://spotify.link/"

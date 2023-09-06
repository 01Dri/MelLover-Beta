from  dotenv import load_dotenv
import os

load_dotenv()
DEFAULT_PATH = os.getcwd()
TOKEN_RIOT = os.getenv("TOKEN_RIOT")
COLOR_FOR_EMBEDS = 0x87CEFA
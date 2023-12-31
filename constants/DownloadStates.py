from enum import Enum


class DownloadStates(Enum):
    FINISH = 0
    IN_PROGRESS = 1
    ERROR = 2

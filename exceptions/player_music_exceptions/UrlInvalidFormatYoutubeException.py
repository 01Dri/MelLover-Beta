class UrlInvalidFormatYoutubeException(Exception):

    def __int__(self, message):
        self.message = message
        super().__init__(self.message)

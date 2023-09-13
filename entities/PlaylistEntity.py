from embeds.Embeds import create_embed_for_playlist_music
from embeds.Embeds import create_embed_for_error_link_music

class PlaylistEntity:

    def __init__(self, title, length, url, description):
        self.title = title
        self.length = length
        self.url = url
        self.description = description



    def get_embed_response(self):
        return create_embed_for_playlist_music(self.title, self.length, self.description)

    def get_emebed_error_response(self):
        return create_embed_for_error_link_music()
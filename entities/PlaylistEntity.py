from embeds.Embeds import create_embed_for_playlist_music


class PlaylistEntity:

    def __init__(self, title, length, track, author, description):
        self.title = title
        self.length = length
        self.track = track
        self.author = author
        self.description = description

    def get_embed_response(self):
        return create_embed_for_playlist_music(self.title, self.length, self.description)

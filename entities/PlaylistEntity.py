from embeds.Embeds import EmbedsCustom
class PlaylistEntity:

    def __init__(self, title, length, description, track, author):
        self.title = title
        self.length = length
        self.description = description
        self.track = track
        self.author = author
        self.embed = EmbedsCustom()
    def get_embed_response(self):
        return self.embed.create_embed_for_playlist_music(self.title, self.length, self.description)

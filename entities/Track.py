from view.view_league_of_legends.ViewEmbedLol import create_embed_for_music_unit, create_embed_for_music_current


class Track():

    def __init__(self, name, time, url, name_discord, url_image_discord) -> None:
        self.name = name
        self.time = time
        self.url = url
        self.name_discord = name_discord
        self.url_image_discord = url_image_discord
        pass

    def get_embed_for_track(self):
        return create_embed_for_music_unit(self.name, self.name_discord)

    def get_embed_for_track_current(self):
        return create_embed_for_music_current(self.name, self.name_discord)

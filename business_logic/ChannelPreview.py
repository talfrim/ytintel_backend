class ChannelPreview:
    """class representing youtube channel preview"""

    def __init__(self, channel_id, title, description, thumbnail_url, video_count, subscriber_count,
                 uploads_playlist_id):
        self.id = channel_id
        self.title = title
        self.description = description
        self.thumbnail_url = thumbnail_url
        self.video_count = video_count
        self.subscriber_count = subscriber_count
        self.uploads_playlist_id = uploads_playlist_id

    # returns the object as a dictionary
    def get_dict(self):
        dictionary = vars(self)
        return dictionary

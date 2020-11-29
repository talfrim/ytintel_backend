class Video:
    """class representing youtube video"""

    def __init__(self, vid_id, title, thumbnail_url, category_id, view_count, like_count, dislike_count,
                 comment_count):
        self.view_count = view_count
        self.category_id = category_id
        self.title = title
        self.thumbnail_url = thumbnail_url
        self.like_count = like_count
        self.dislike_count = dislike_count
        self.comment_count = comment_count
        self.comment_list = []
        self.bad_comments = -1
        self.good_comments = -1
        self.good_comments_rate = 0

    def get_dict(self):
        dictionary = vars(self)
        return dictionary

    def add_good_comment(self):
        self.good_comments += 1

    def add_bad_comment(self):
        self.bad_comments += 1

    def calc_good_comments_rate(self):
        self.good_comments_rate = self.good_comments / self.comment_count if self.comment_count > 0 else -1


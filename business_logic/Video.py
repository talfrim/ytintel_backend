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
        self.neutral_comments = -1

        self.top_comments = []

    def get_dict(self):
        dictionary = vars(self)
        return dictionary

    def add_good_comment(self):
        self.good_comments += 1

    def add_bad_comment(self):
        self.bad_comments += 1

    def add_neutral_comment(self):
        self.neutral_comments += 1

    def analyze_comments(self):
        for c in self.comment_list:
            c.analyze_sentiment()
            if c.sentiment == 1:
                self.add_good_comment()
            if c.sentiment == 0:
                self.add_neutral_comment()
            if c.sentiment == -1:
                self.add_bad_comment()

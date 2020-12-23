class Video:
    """class representing youtube video"""

    def __init__(self, vid_id, title, description, published_at, thumbnail_url, category_id, view_count, like_count, dislike_count,
                 comment_count):
        self.view_count = view_count
        self.category_id = category_id
        self.title = title
        self.description = description
        self.published_at = published_at
        self.thumbnail_url = thumbnail_url
        self.like_count = like_count
        self.dislike_count = dislike_count
        self.comment_count = comment_count
        self.bad_comments = -1
        self.good_comments = -1
        self.neutral_comments = -1
        self.top_comments = []  # list of strings

    def get_dict(self):
        dct_comments = []
        for c in self.top_comments:
            dct_comments.append(c.get_dict())
        self.top_comments = dct_comments    # turning comments to dicts, note: destroys the comment list, if it is needed should be iplemented differently
        dictionary = vars(self)
        return dictionary

    def set_top_comments_lst(self, lst):
        self.top_comments = lst

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
        self.comment_list = None
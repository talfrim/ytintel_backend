class Comment:

    # At first comment will not have sentiment, after running it through the semantic analyzer
    # is will be updated
    def __init__(self, text, author, likes, video_id):
        self.video_id = video_id
        self.text = text
        self.author = author
        self.likes = likes
        self.sentiment = None

    def set_sentiment(self, sentiment):
        self.sentiment = sentiment

    def analyze_sentiment(self):
        self.set_sentiment(1)

    def get_dict(self):
        dictionary = vars(self)
        return dictionary

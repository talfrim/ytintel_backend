from business_logic.semantic_analyzer.CommentAnalyzer import CommentAnalyzer


class Comment:

    # At first comment will not have sentiment, after running it through the semantic analyzer
    # is will be updated
    def __init__(self, text, author, likes, video_id):
        self.video_id = video_id
        self.text = text
        self.author = author
        self.likes = likes
        self.sentiment = None
        self.comment_analyzer = CommentAnalyzer.getInstance()

    def set_sentiment(self, sentiment):
        self.sentiment = sentiment

    def analyze_sentiment(self):
        sentiment = self.comment_analyzer.analyze_text(self.text)
        self.set_sentiment(sentiment)

    def get_dict(self):
        self.comment_analyzer = None
        dictionary = vars(self)
        return dictionary

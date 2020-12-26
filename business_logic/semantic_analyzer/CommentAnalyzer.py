from joblib import dump, load
import pandas as pd
import nltk
from nltk.stem.snowball import EnglishStemmer
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.stem import PorterStemmer
import scipy.sparse
nltk.download('punkt')




""" A singleton class that reads the model and can
analyze comments. Do not use the constructor,
use getInstance()"""
class CommentAnalyzer:

    __instance = None

    @staticmethod
    def getInstance():
        """ Static access method. """
        if CommentAnalyzer.__instance is None:
            CommentAnalyzer()
        return CommentAnalyzer.__instance

    def __init__(self):
        """ Virtually private constructor. """
        if CommentAnalyzer.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            self.clf = load('business_logic\semantic_analyzer\lr_model.joblib')  # loading model
            self.porter = PorterStemmer()
            self.stemmer = EnglishStemmer()
            self.count_vectorizer = load('business_logic/semantic_analyzer/count_vectorized.joblib')
            self.tfidf_vectorizer = load('business_logic/semantic_analyzer/tfidf_vectorized.joblib')
            CommentAnalyzer.__instance = self


    """ The actual method that analyzes text """
    def analyze_text(self, text):
        total_train_vectorizer = self.get_final_vectorizer(text)
        result = self.clf.predict(total_train_vectorizer)[0]
        if result == 'positive':
            return 1
        if result == 'negative':
            return -1
        else:
            return 0 # neutral


    # returns sparse matrix with all the features of the given text.
    def get_final_vectorizer(self, text):
        # insert to df
        df = pd.DataFrame(columns=['text'])
        comment_row = [text]
        df.loc[len(df), :] = comment_row
        # preprocess
        df['text'] = df['text'].apply(self.preprocessing)  # lowering the text
        df['text'] = df.apply(lambda row: self.stemParagraph(row.text), axis=1)  # stemming
        count_vectorized = self.count_vectorizer.transform(df['text'])  # generating feature of bag of words with 1-2 grams
        tfidf_vectorized = self.tfidf_vectorizer.transform(df['text'])  # generating feature of tfidf with 1-3 grams
        total_train_vectorizer = scipy.sparse.hstack([tfidf_vectorized, count_vectorized])  # appending all features to sparse matrix
        return total_train_vectorizer

    # returns the stemmed paragraph from the given paragraph.
    def stemParagraph(self, paragraph):
        token_words = word_tokenize(paragraph)
        stem_paragraph = []
        for word in token_words:
            stem_paragraph.append(self.stemmer.stem(word))
            stem_paragraph.append(" ")
        return "".join(stem_paragraph)

    # pre-processing the document
    def preprocessing(self, doc):
        # lowercase the words in the doc
        doc = doc.lower()
        return doc

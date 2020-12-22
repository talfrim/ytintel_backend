from joblib import dump, load
import numpy as np
import pandas as pd
import sklearn as sk
import nltk
nltk.download('punkt')
import re
from nltk.stem.snowball import EnglishStemmer
from sklearn.feature_extraction import text
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.stem import PorterStemmer
from sklearn.model_selection import train_test_split
import scipy.sparse
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
import time
import matplotlib.pyplot as plt
import seaborn as sns



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
            self.clf = load('lr_model.joblib')  # loading model
            self.porter = PorterStemmer()
            self.stemmer = EnglishStemmer()
            self.count_vectorizer = CountVectorizer(ngram_range=(1, 2), stop_words='english')
            self.tfidf_vectorizer = TfidfVectorizer(ngram_range=(1, 3), stop_words='english')
            CommentAnalyzer.__instance = self


    """ The actual method that analyzes text"""
    def analyze_text(self, text):
        total_train_vectorizer = self.get_final_vectorizer(text)
        result = self.clf.predict(total_train_vectorizer)
        print(result)


    def get_final_vectorizer(self, text):
        # insert to df
        df = pd.DataFrame(columns=['text'])
        comment_row = [text]
        df.loc[len(df), :] = comment_row
        # preprocess
        df['text'] = df['text'].apply(self.preprocessing)  # lowering the text
        df['text'] = df.apply(lambda row: self.stemParagraph(row.text), axis=1)  # stemming
        count_vectorized = self.count_vectorizer.fit_transform(df['text'])  # generating feature of bag of words with 1-2 grams
        tfidf_vectorized = self.tfidf_vectorizer.fit_transform(df['text'])  # generating feature of tfidf with 1-3 grams
        total_train_vectorizer = scipy.sparse.hstack([tfidf_vectorized, count_vectorized])  # appending all features to sparse matrix
        return total_train_vectorizer


    def stemParagraph(self, paragraph):
        token_words = word_tokenize(paragraph)
        token_words
        stem_paragraph = []
        for word in token_words:
            stem_paragraph.append(self.stemmer.stem(word))
            stem_paragraph.append(" ")
        return "".join(stem_paragraph)

    def preprocessing(self, doc):
        doc = doc.lower()
        return doc


ca = CommentAnalyzer.getInstance()
ca.analyze_text("Very good comment, great")

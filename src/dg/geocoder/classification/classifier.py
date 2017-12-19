import pickle

from nltk.corpus import stopwords
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.svm.classes import LinearSVC
from sklearn.naive_bayes import MultinomialNB
from sklearn.tree.tree import DecisionTreeClassifier

from dg.geocoder.config import get_classifiers_path

english_stops = stopwords.words('english')


class Classifier:
    def __init__(self):
        self.clf = LinearSVC()
        self.scores = []
        self.vectorizer = CountVectorizer(token_pattern=r'[A-z]+',  stop_words=english_stops,
                                          ngram_range=(1, 1))

    def predict(self, texts):
        return self.clf.predict(self.vectorizer.transform(texts))

    def train(self, x, y):
        self.clf.fit(self.vectorizer.fit_transform(x), y)

    def save(self, name, path=get_classifiers_path()):
        pickle.dump(self, open("{}/{}.p".format(path, name), "wb"))
        return self.clf


def load_classifier(name, path=get_classifiers_path()):
    return pickle.load(open(("{}/{}.p".format(path, name)), "rb"))

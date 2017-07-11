from nltk import RegexpTokenizer, LancasterStemmer
from nltk.stem.wordnet import WordNetLemmatizer


class LemmaTokenizer(object):
    def __init__(self):
        self.wnl = WordNetLemmatizer()

    def __call__(self, doc):
        return [self.wnl.lemmatize(t) for t in RegexpTokenizer(r'[A-z]+').tokenize(doc)]


class StemmTokenizer(object):
    def __init__(self):
        self.stm = LancasterStemmer()

    def __call__(self, doc):
        return [self.stm.stem(t) for t in RegexpTokenizer(r'[A-z]+').tokenize(doc)]

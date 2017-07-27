import nltk
from langdetect.detector_factory import detect
punk_tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')

class BaseReader:
    def __init__(self, file):
        self.paragraphs = []
        # split pd in paragraphs

    def get_sample(self):
        pass

    def is_english_lan(self):
        return detect(self.get_sample()) == 'en'


def get_sentence_tokenizer():
    return punk_tokenizer

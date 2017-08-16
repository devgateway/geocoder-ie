import nltk
from langdetect.detector_factory import detect
from nltk.tokenize.texttiling import TextTilingTokenizer


class BaseReader:
    def __init__(self, file):
        self.paragraphs = []
        # split pd in paragraphs

    def get_sample(self):
        pass

    def is_english_lan(self):
        print('Detecting document language ')
        return detect(self.get_sample()) == 'en'


def get_sentence_tokenizer():
    punk_tokenizer = nltk .data.load('tokenizers/punkt/english.pickle')
    return punk_tokenizer
    #TextTilingTokenizer(demo_mode=False)

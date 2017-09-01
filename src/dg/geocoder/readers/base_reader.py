import logging

import nltk
from langdetect.detector_factory import detect

logger = logging.getLogger()


class BaseReader:
    def __init__(self):
        self.paragraphs = []
        # split pd in paragraphs

    def get_sample(self):
        pass

    def is_english_lan(self):
        logger.info('Detecting document language ')
        return detect(self.get_sample()) == 'en'


def get_sentence_tokenizer():
    punk_tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
    return punk_tokenizer

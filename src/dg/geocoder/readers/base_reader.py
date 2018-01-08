import logging

import nltk
from langdetect.detector_factory import detect
from langdetect.lang_detect_exception import LangDetectException
from orca.debug import println

logger = logging.getLogger()


class BaseReader:
    def __init__(self):
        self.paragraphs = []
        # split pd in paragraphs

    def get_sample(self):
        pass

    def get_file_name(self):
        if self.file:
            return self.file.split('/')[-1]

    def is_english_lang(self):
        try:
            logger.info('Detecting language ({})'.format(self.get_file_name()))
            return detect(self.get_sample()) == 'en'
        except LangDetectException as err:
            logger.error("Wasn't able to detect language")
            return False


def get_sentence_tokenizer():
    punk_tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
    return punk_tokenizer

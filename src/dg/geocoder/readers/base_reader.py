import logging

import nltk
from langdetect.detector_factory import detect
from langdetect.lang_detect_exception import LangDetectException
from dg.geocoder.util.file_util import get_file_name

logger = logging.getLogger()


class BaseReader:
    def __init__(self):
        self.paragraphs = []

    def get_sample(self):
        pass

    def text_language(self):
        try:
            logger.info('Detecting language ({})'.format(get_file_name(self._file)))
            sample = self.get_sample()
            if sample and sample.strip():
                return detect(sample)
            else:
                logger.info("Can't detect lang , string is empty")
                return 'en'
        except LangDetectException as err:
            logger.error(err)
            logger.error("Wasn't able to detect language")
            return False

    def is_french_lang(self):
        return self.text_language == 'fr'

    def is_english_lang(self):
        return self.text_language == 'en'

    def get_sentence_tokenizer(self):
        punk_tokenizer = None

        if self.text_language == 'en':
            punk_tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
        if self.text_language == 'fr':
            punk_tokenizer = nltk.data.load('tokenizers/punkt/PY3/french.pickle')

        if punk_tokenizer is None:
            punk_tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')

        return punk_tokenizer

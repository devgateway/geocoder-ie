# -*- coding: utf-8 -*-
import PyPDF2
import re

import nltk
from nltk.tokenize.regexp import regexp_tokenize, RegexpTokenizer


class PdfReader:
    def __init__(self, file):
        self.file = file
        self.paragraphs = []
        self.reader = PyPDF2.PdfFileReader(open(self.file, 'rb'))
        self.sentence_tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
        # split pd in paragraphs

    def split(self):
        if len(self.paragraphs) == 0:
            reg_exp = RegexpTokenizer(r'\w+([.,]\w+)*|\S+')
            for page in self.reader.pages[2:]:
                raw_text = self.read_page(page)
                ps = self.sentence_tokenizer.tokenize(raw_text)
                for s in ps:
                    if len(s) > 150:
                        self.paragraphs.append(s)

        return self.paragraphs

    # Extract raw text from page number
    def get_page(self, n):
        return self.read_page(self.reader.getPage(n))

    # Extract raw text from page
    def read_page(self, page):
        return page.extractText()

    def get_paragraphs(self):
        return self.paragraphs

    def get_pages_text(self):
        return self.texts

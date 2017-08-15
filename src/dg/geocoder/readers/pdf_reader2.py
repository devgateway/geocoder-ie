# -*- coding: utf-8 -*-
from PyPDF2.pdf import PdfFileReader
from xpdf_python import to_text

from dg.geocoder.readers.base_reader import BaseReader, get_sentence_tokenizer


class PdfReader(BaseReader):
    def __init__(self, file):
        self.file = file
        self.paragraphs = []
        # split pd in paragraphs

    def read(self, n):
        text = to_text( self.file )

        reader = PdfFileReader(self.file)
        content = ""
        if n is None:
            n = reader.getNumPages()
        for i in range(0, n):
            content += reader.getPage(i).extractText() + '\n'

        return content

    def split(self, n=None):
        print('Splitting document in sentences')
        if len(self.paragraphs) == 0:
            raw_text = self.read(n)
            tokenizer = get_sentence_tokenizer()
            tokens = tokenizer.tokenize(raw_text)
            for t in tokens:
                self.paragraphs.append(t)

        return self.paragraphs

    def get_paragraphs(self):
        return self.paragraphs

    def get_pages_text(self):
        return self.texts

    def get_sample(self):
        return self.read(1)

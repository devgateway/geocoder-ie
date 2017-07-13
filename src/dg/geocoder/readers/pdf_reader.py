# -*- coding: utf-8 -*-
import PyPDF2
import re


class PdfReader:
    def __init__(self, file):
        self.file = file
        self.paragraphs = []
        self.reader = PyPDF2.PdfFileReader(open(self.file, 'rb'))

        # split pd in paragraphs

    def split(self):
        if len(self.paragraphs) == 0:
            for page in self.reader.pages:
                raw_text = self.read(page)
                ps = re.split('/\n/', raw_text)
                self.paragraphs = +ps

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

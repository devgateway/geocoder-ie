# -*- coding: utf-8 -*-
import PyPDF2
import re

class Pdfreader:
    def __init__(self, file):
        self.file = file

        ##returns text collection

    def read(self):
        bfile = open(self.file, 'rb')
        reader = PyPDF2.PdfFileReader(bfile)
        page = reader.getPage(0)
        self.paragraphs= []
        self.texts = []
        for page in reader.pages:
            raw_text = page.extractText()
            self.texts.append(raw_text)
            paragprahs=re.split('/\n/',raw_text)
            for p in paragprahs:
                self.paragraphs.append(p)

    def get_paragraphs(self):
        return self.paragraphs

    def get_pages_text(self):
        return self.texts


# -*- coding: utf-8 -*-
import io
import re

from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage

from dg.geocoder.readers.base_reader import BaseReader, get_sentence_tokenizer


class PdfReader(BaseReader):
    def __init__(self, file):
        self.file = file
        self.paragraphs = []
        # split pd in paragraphs

    def convert_pdf_to_txt(self, limit=20):
        rsrcmgr = PDFResourceManager()
        retstr = io.StringIO()
        codec = 'utf-8'
        laparams = LAParams()
        device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
        fp = open(self.file, 'rb')
        interpreter = PDFPageInterpreter(rsrcmgr, device)
        password = ""
        maxpages = 0
        caching = True
        pagenos = set()
        i = 0
        for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages,
                                      password=password,
                                      caching=caching,
                                      check_extractable=True):
            print('Reading pdf page {}'.format(i))
            interpreter.process_page(page)

            i = i + 1

        text = retstr.getvalue()

        fp.close()
        device.close()
        retstr.close()
        return text

    def split(self, limit=20):
        print('Splitting document in sentences')
        if len(self.paragraphs) == 0:
            raw_text = self.convert_pdf_to_txt()
            tokenizer = get_sentence_tokenizer()
            texts = re.split('/\n/', raw_text)
            ps = []
            for t in texts:
                tokens = tokenizer.tokenize(t)
                for s in tokens:
                    ps.append(s)
            for s in ps:
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

    def get_sample(self):
        return self.get_page(1)

# -*- coding: utf-8 -*-
import io
import logging
import sys

from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage

from dg.geocoder.readers.base_reader import BaseReader, get_sentence_tokenizer

logger = logging.getLogger()


class PdfReader(BaseReader):
    def __init__(self, file):
        super().__init__()
        self.file = file
        self.paragraphs = []
        # split pd in paragraphs

    def convert_pdf_to_txt(self, pagenos=None, verbose=True):

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
        pagenos = set(pagenos) if pagenos is not None else set()
        i = 0
        if verbose:
            print('')
            print('Reading pdf pages '.format(i + 1), end=' ')

        for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages,
                                      password=password,
                                      caching=caching,
                                      check_extractable=True):
            if verbose:
                print('{}'.format(i + 1), end=' ')
                sys.stdout.flush()

            interpreter.process_page(page)

            i = i + 1
        if verbose:
            print('\n')


        text = retstr.getvalue()

        fp.close()
        device.close()
        retstr.close()
        return text

    def split(self, pagenos=None):
        logger.info('Splitting document in sentences')
        if len(self.paragraphs) == 0:
            raw_text = self.convert_pdf_to_txt(pagenos)
            tokenizer = get_sentence_tokenizer()
            tokens = tokenizer.tokenize(raw_text)
            for t in tokens:
                self.paragraphs.append(t)

        return self.paragraphs

    # Extract raw text from page
    def read_page(self, page):
        return page.extractText()

    def get_paragraphs(self):
        return self.paragraphs

    def get_pages_text(self):
        return self.texts

    def get_sample(self):
        return self.convert_pdf_to_txt(pagenos=[2], verbose=False)

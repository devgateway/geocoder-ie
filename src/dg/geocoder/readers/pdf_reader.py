# -*- coding: utf-8 -*-
import io
import logging
import random
import sys

from pdfminer.converter import TextConverter, PDFPageAggregator
from pdfminer.layout import LAParams, LTTextBox, LTTextLine
from pdfminer.pdfdevice import PDFDevice
from pdfminer.pdfdocument import PDFDocument, PDFTextExtractionNotAllowed
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfparser import PDFParser, PDFSyntaxError

from dg.geocoder.readers.base_reader import BaseReader, get_sentence_tokenizer

logger = logging.getLogger()


def read_page(page):
    return page.extractText()


class PdfReader(BaseReader):
    def __init__(self, file):
        super().__init__()
        self.file = file
        self.paragraphs = []
        # split pd in paragraphs

    def read(self, pagenos=None, verbose=True):
        try:
            if verbose:
                logger.info('Reading file {}'.format(self.get_file_name()))

            extracted_text = ""
            # Open a PDF file.
            fp = open(self.file, 'rb')
            # Create a PDF parser object associated with the file object.
            # parser = PDFParser(fp)
            # Create a PDF document object that stores the document structure.
            # Supply the password for initialization.
            # document = PDFDocument(parser, "")
            # Check if the document allows text extraction. If not, abort.
            # if not document.is_extractable:
            #   raise PDFTextExtractionNotAllowed
            # Create a PDF resource manager object that stores shared resources.
            rsrcmgr = PDFResourceManager()
            # Create a PDF device object.
            device = PDFDevice(rsrcmgr)
            laparams = LAParams()

            pagenos = set(pagenos) if pagenos is not None else set()
            device = PDFPageAggregator(rsrcmgr, laparams=laparams)

            # Create a PDF interpreter object.
            interpreter = PDFPageInterpreter(rsrcmgr, device)
            # Process each page contained in the document.

            i = 0
            if verbose:
                print('')
                print('Reading pdf pages '.format(i + 1), end=' ')

            for page in PDFPage.get_pages(fp, pagenos=pagenos, caching=True):
                if verbose:
                    print('{}'.format(i + 1), end=' ')
                    sys.stdout.flush()
                # As the interpreter processes the page stored in PDFDocument object
                interpreter.process_page(page)
                # The device renders the layout from interpreter
                layout = device.get_result()
                # Out of the many LT objects within layout, we are interested in LTTextBox and LTTextLine
                for lt_obj in layout:
                    if isinstance(lt_obj, LTTextBox) or isinstance(lt_obj, LTTextLine):
                        extracted_text += lt_obj.get_text()
                        # interpreter.process_page(page)
                i = i + 1

            if verbose:
                print('\n')

            device.close()
            fp.close()
            return extracted_text
        except PDFSyntaxError as syntaxError:
            logger.error("FIle {} seems to have a wrong format or it is empty".format(self.get_file_name()))
            return ""

    def get_page_numbers(self):
        try:
            fp = open(self.file, 'rb')
            parser = PDFParser(fp)
            document = PDFDocument(parser, "")
            pages = [index for index, page in enumerate(PDFPage.get_pages(fp, check_extractable=False))]
            fp.close()
            return pages
        except PDFSyntaxError as error:
            logger.error("Can read this document please check file {}".format(self.get_file_name()))

    def split(self, pagenos=None):
        logger.info('Splitting document in sentences')
        if len(self.paragraphs) == 0:
            raw_text = self.read(pagenos)
            tokenizer = get_sentence_tokenizer()
            tokens = tokenizer.tokenize(raw_text)
            for t in tokens:
                self.paragraphs.append(t)

        return self.paragraphs

    # Extract raw text from page

    def get_paragraphs(self):
        return self.paragraphs

    def get_sample(self):
        try:
            pages = self.get_page_numbers()
            samples = 2 if len(pages) > 1 else 1
            numbers = random.sample(pages, samples)
            return self.read(pagenos=numbers, verbose=False)
        except ValueError as error:
            logger.error(error)

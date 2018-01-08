import unittest

import time

from dg.geocoder.geo.geocoder import merge, join
from dg.geocoder.readers import pdf_reader
from dg.geocoder.readers.factory import get_reader
from dg.geocoder.readers.pdf_reader import PdfReader


class TestReaders(unittest.TestCase):
    def test_image(self):
        reader = PdfReader('resources/image.pdf')
        self.assertFalse(reader.is_english_lang())

    def test_pdf(self):
        reader = PdfReader('resources/afdb_subnational.pdf')



        self.assertTrue(reader.is_english_lang())




if __name__ == '__main__':
    unittest.main()

import unittest

from dg.geocoder.readers.factory import get_reader


class TestGeocoder(unittest.TestCase):
    def test_tokenizer_pdf(self):
        reader = get_reader('src\\test\\tonkenize.pdf')
        tokens = reader.split
        for s in tokens:
            logger.info(s)
            logger.info('.' * 120)
            logger.info('|' * 120)

    def test_tokenizer_odt(self):
        reader = get_reader('src\\test\\tokenize.odt')
        tokens = reader.split
        for s in tokens:
            logger.info(s)
            logger.info('.' * 120)
            logger.info('|' * 120)


if __name__ == '__main__':
    unittest.main()

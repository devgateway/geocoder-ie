import unittest

from dg.geocoder.processor import process_file


class TestGeocoder(unittest.TestCase):

    def test_json_output(self):
        print('Test Json')
        process_file('resources/afdb_subnational.pdf')

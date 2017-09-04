import unittest

from dg.geocoder.geo.geonames import resolve


class TestGeoNames(unittest.TestCase):
    def test_country_name(self):
        resolve('Kenya', cty_codes=[])

    def test_incomplete_name(self):
        resolve('Dhaka South', cty_codes=[])['name'] == 'Dhaka South City Corporation'

    def test_strange_name(self):
        resolve('FSD', cty_codes=[])


if __name__ == '__main__':
    unittest.main()

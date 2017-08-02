import unittest

from dg.geocoder.geo.geocoder import geocode


class TestGeocoder(unittest.TestCase):
    def test_geocode(self):
        text = """During this period, PRIME expanded to include 4 new upazilas 
                    (Tala in Satkhira district and Islampur, Dewanganj and Melandaha in Jamalpur district) 
                        to serve large numbers of poor people in these adjacent areas."""

        print(geocode(text=text))


if __name__ == '__main__':
    unittest.main()
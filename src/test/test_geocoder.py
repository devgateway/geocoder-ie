import unittest

from dg.geocoder.geo.geocoder import geocode, merge


class TestGeocoder(unittest.TestCase):
    def test_geocode(self):
        text = """During this period, PRIME expanded to include 4 new upazilas 
                    (Tala in Satkhira district and Islampur, Dewanganj and Melandaha in Jamalpur district) 
                        to serve large numbers of poor people in these adjacent areas"""
        geo = geocode(text=text,country_codes=['BD'])

    def test_merge(self):
        text = "Congo,New Guinea and Burkina Faso, same as the route Cordoba-Catamarca, Democratic Republic of Congo"
        entities = ['Congo', 'New', 'Guinea', 'Burkina Faso', 'Cordoba', 'Catamarca', 'Democratic', 'Republic', 'of',
                    'Congo']
        rels = []
        extraction = []
        extraction.append(({'text': text, 'entities': entities, 'relations': []}))
        results = merge(extraction)
        self.assertTrue('New Guinea' in results[0]['locations'])
        self.assertTrue('Cordoba' in results[0]['locations'])
        self.assertTrue('Burkina Faso' in results[0]['locations'])
        self.assertTrue('Democratic Republic of Congo' in results[0]['locations'])

    if __name__ == '__main__':
        unittest.main()

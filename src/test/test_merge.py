import unittest

from dg.geocoder.geo.geocoder import merge, extract, join, geonames
from dg.geocoder.readers.factory import get_reader, get_text_reader


class TestMerge(unittest.TestCase):
    def test_merge(self):
        text = "Congo,New Guinea and Burkina Faso, same as the route Cordoba-Catamarca, Democratic Republic of Congo"
        entities = ['Congo', 'New', 'Guinea', 'Burkina Faso', 'Cordoba', 'Catamarca', 'Democratic', 'Republic', 'of',
                    'Congo']
        rels = []
        extraction = [{'text': text, 'entities': entities, 'relations': []}]
        results = merge(extraction)
        self.assertTrue('New Guinea' in results[0]['locations'])
        self.assertTrue('Cordoba' in results[0]['locations'])
        self.assertTrue('Burkina Faso' in results[0]['locations'])
        self.assertTrue('Democratic Republic of Congo' in results[0]['locations'])

    def test_merge_1(self):
        text = get_reader('resources/sample_text_1.txt').split()[0]
        entities = ['Burkina', 'Faso', 'Bissiga', 'Central', 'Plateau', 'Region']
        extraction = [{'text': text, 'entities': entities, 'relations': []}]

        results = merge(extraction)
        self.assertTrue('Central Plateau Region' in results[0]['locations'])

    def test_merge_2(self):
        text = get_reader('resources/sample_text_2.txt').split()[0]
        entities = ['Benin', 'Benin', 'Burkina', 'Faso', 'Ghana', 'Mozambique']
        ner_decorated = [{'text': text, 'entities': entities, 'relations': []}]

        merge_decorated = merge(ner_decorated)
        normalized = join(merge_decorated)
        found = [l for l, data in normalized]
        self.assertTrue('Benin' in found)
        self.assertTrue('Ghana' in found)
        self.assertTrue('Mozambique' in found)
        self.assertTrue('Burkina Faso' in found)

    def test_merge_new_lines(self):
        text="""Dadieso Forest
Reserves

Kakum National Park area, Central Region"""

        entities = ['Dadieso', 'Forest', 'Reserves', 'Kakum', 'National', 'Park']
        ner_decorated = [{'text': text, 'entities': entities, 'relations': []}]
        merge_decorated = merge(ner_decorated, ignored_gap_chars=[','])
        print(merge_decorated)

if __name__ == '__main__':
    unittest.main()

import json
import logging.config
import unittest

from dg.geocoder.config import get_log_config_path
from dg.geocoder.geo.geocoder import geonames
from dg.geocoder.geo.geocoder import merge, join, extract_spacy
from dg.geocoder.readers.json_reader import JsonReader
import rpyc

logging.config.fileConfig(get_log_config_path())
logger = logging.getLogger()


class TestJsonReader(unittest.TestCase):
    def test_json(self):
        json_file = open('resources/allActivityDocuments.json', 'r')
        j_object = json.load(json_file)

        for activity in j_object:
            reader = JsonReader(activity)
            text = reader.split()
            ner_decorated = extract_spacy(text)
            merge_decorated = merge(ner_decorated)
            normalized = join(merge_decorated)
            found = [l for l, data in normalized]
            geonames(normalized, ['DO', 'HT'])
            json_file.close()

    def test_extraction(self):
        # conn = rpyc.connect("localhost", 18861, config={"sync_request_timeout": 30})
        ner_decorated = extract_spacy([(
            "The Project consists of the construction and operation of an apparel manufacturing facility in the municipality of Croix-des-Bouquets, Haiti that will produce high-end, quality garments for export to the North American market.",
            "objetives")])
        merge_decorated = merge(ner_decorated)
        normalized = join(merge_decorated)
        found = [l for l, data in normalized]
        geocoding = geonames(normalized, ['DO', 'HT'])
        self.assertTrue('Arrondissement de Croix des Bouquets' in [b['geocoding']['name'] for a, b in geocoding])


    def test_extraction(self):
        # conn = rpyc.connect("localhost", 18861, config={"sync_request_timeout": 30})
        ner_decorated = extract_spacy([(
            "Ce projet consiste en la reconstruction de quatre commissariats de police (à Léogâne, Gressier, Grand-Goâve et Côtes-de-Fer), un tribunal de paix (à Kenscoff) et d’un tribunal de première instance (à Croix-des-Bouquets).",
            "objetives")])
        merge_decorated = merge(ner_decorated)
        normalized = join(merge_decorated)
        found = [l for l, data in normalized]
        print(found)
        geocoding = geonames(normalized, ['DO', 'HT'])
        self.assertTrue('Arrondissement de Croix des Bouquets' in [b['geocoding']['name'] for a, b in geocoding])

if __name__ == '__main__':
    unittest.main()

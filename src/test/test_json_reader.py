import json
import unittest
from dg.geocoder.geo.geocoder import merge, join, geonames
import spacy
from dg.geocoder.readers.factory import get_reader
from dg.geocoder.readers.json_reader import JsonReader


class TestJsonReader(unittest.TestCase):
    def test_json(self):
        nlp = spacy.load('fr_core_news_md')
        json_file = open('resources/allActivityDocuments.json', 'r')
        j_object = json.load(json_file)
        done_items = []
        total = len(j_object)
        current = 0
        for activity in j_object:
            activity['auto_geocoder'] = []
            current = current + 1
            if current > 10:
                break

            print('Processing %s of %s', current, total)
            reader = JsonReader(activity)
            paragraphs = reader.split()
            print(activity['amp_id'])
            items = []

            pos = 0
            for doc in nlp.pipe([a for a, b in paragraphs], disable=["tagger", "parser"]):
                # Do something with the doc here
                locations = [ent.text for ent in doc.ents if ent.label_ in 'LOC']

                if len(locations) > 0:
                    items = [(l, {'field': paragraphs[pos][1], 'text': doc.text}) for l in locations]

                pos = pos + 1

            geo_coding = geonames(items, ['HTI'])
            activity['auto_geocoder'] = geo_coding
            done_items.append({'amp_id': activity.amp_id, 'geo_coding': geo_coding})

        with open('resources/allActivityDocuments_geocoded.json', 'w') as outfile:
            json.dump(done_items, outfile)

        json_file.close()


if __name__ == '__main__':
    unittest.main()

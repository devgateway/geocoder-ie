import json
import logging, logging.config
import sys

from dg.geocoder.config import get_log_config_path
from dg.geocoder.data.activities_corpora_generator import load_activities_corpora
from dg.geocoder.geo.geocoder import geonames, extract_ner, merge, join
from dg.geocoder.readers.json_reader import JsonReader

logging.config.fileConfig(get_log_config_path())
logger = logging.getLogger('sLogger')

def main(args):
    logger.info("Starting")
    json_file = open('test/resources/allActivityDocuments.json', 'r')
    j_object = json.load(json_file)
    i = 0
    for activity in j_object:
        logger.info("Geocoding Activity " + activity["amp_id"])
        reader = JsonReader(activity)
        text = reader.split()

        ner_decorated = extract_ner(text)
        merge_decorated = merge(ner_decorated)
        normalized = join(merge_decorated)
        geocoding = geonames(normalized, ['DO', 'HT'])

        print(geocoding)


if __name__ == '__main__':
    main(sys.argv[1:])
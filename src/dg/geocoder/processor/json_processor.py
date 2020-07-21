import logging

from dg.geocoder.config import get_log_config_path, get_download_path
from dg.geocoder.geo.geocoder import geocode, extract_spacy, merge, join, geonames
from dg.geocoder.iati.iati_downloader import download_activity_data
from dg.geocoder.processor.base_processor import BaseProcessor
import json

from dg.geocoder.readers.json_reader import JsonReader

logger = logging.getLogger()


class JsonProcessor(BaseProcessor):
    def __init__(self, json, **kwargs):
        BaseProcessor.__init__(self, json, **kwargs)
        self.document = json

    def process(self):
        logger.info('processing json file {}'.format(self.document))
        j_object = json.load(self.document)
        i = 0
        for activity in j_object:
            reader = JsonReader(activity)
            text = reader.split()
            ner_decorated = extract_spacy(text)
            merge_decorated = merge(ner_decorated)
            normalized = join(merge_decorated)
            geocoding = geonames(normalized, ['HT'])
            self.locations = geocoding
        return self

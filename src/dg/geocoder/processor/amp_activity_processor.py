import logging

from dg.geocoder.config import get_default_country
from dg.geocoder.geo.geocoder import extract_ner, merge, join, geonames
from dg.geocoder.processor.base_processor import BaseProcessor

logger = logging.getLogger()


class AmpActivityProcessor(BaseProcessor):
    def __init__(self, activity, **kwargs):
        BaseProcessor.__init__(self, activity, **kwargs)
        self.activity = activity
        self.results = None
        self.locations = []

    # Geocode AMP activity
    def process(self):
        logger.info('.......... Coding activity {} ..........'.format(self.activity.get_identifier()))
        text = self.activity.split()

        ner_decorated = extract_ner(text)
        merge_decorated = merge(ner_decorated)
        normalized = join(merge_decorated)
        self.results = geonames(normalized, get_default_country())

        self.locations.append((self.activity.get_identifier(),
                               [data['geocoding'] for (l, data) in self.results if data.get('geocoding')]))
        return self

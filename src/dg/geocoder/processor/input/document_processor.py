import logging.config

from dg.geocoder.config import get_log_config_path
from dg.geocoder.geo.geocoder import geocode

logging.config.fileConfig(get_log_config_path())
logger = logging.getLogger()


class DocumentProcessor():
    def __init__(self, document, cty_codes=[]):
        self.document = document
        self.results = []
        self.locations = []
        self.cty_codes = cty_codes

    def process(self):
        logger.info('processing document {}'.format(self.document))
        self.results = geocode([], [self.document], cty_codes=self.cty_codes)
        self.locations = [(data['geocoding'], data['texts']) for (l, data) in self.results if data.get('geocoding')]

    def get_locations(self):
        return self.locations

    def get_results(self):
        return self.results

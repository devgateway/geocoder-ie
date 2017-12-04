import logging.config

from dg.geocoder.config import get_log_config_path
from dg.geocoder.geo.geocoder import geocode
from dg.geocoder.processor.base_processor import BaseProcessor

logging.config.fileConfig(get_log_config_path())
logger = logging.getLogger()


class DocumentProcessor(BaseProcessor):
    def __init__(self, document, **kwargs):
        BaseProcessor.__init__(self, document, **kwargs)
        self.document = document

    def process(self):
        logger.info('processing document {}'.format(self.document))
        self.results = geocode([], [self.document], cty_codes=self.cty_codes)
        self.locations = [((self.document,
                            [data['geocoding'] for (l, data) in self.results if data.get('geocoding')]))]

        return self

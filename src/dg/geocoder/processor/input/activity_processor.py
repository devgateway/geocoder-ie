import logging

from dg.geocoder.config import get_log_config_path, get_download_path
from dg.geocoder.geo.geocoder import geocode
from dg.geocoder.iati.iati_downloader import download_activity_data
from dg.geocoder.processor.input.base_processor import BaseProcessor

logging.config.fileConfig(get_log_config_path())
logger = logging.getLogger()


class ActivityProcessor(BaseProcessor):
    def __init__(self, activity, **kwargs):
        BaseProcessor.__init__(self, activity, **kwargs)
        self.activity = activity
        self.results = None
        self.locations = []

    # Geocode a IATI activity
    def process(self):
        logger.info('.......... Coding activity {} ..........'.format(self.activity.get_identifier()))
        # Get activity related documents
        documents = download_activity_data(self.activity, get_download_path())
        # extract title and descriptions a
        texts = self.activity.get_texts()
        # call full geocode workflow
        # TODO CHECK if country code can be an array
        # full results
        self.results = geocode(texts, documents, cty_codes=self.activity.get_recipient_country_code())

        # add location to activity
        [self.activity.add_location(data['geocoding']) for (l, data) in self.results if data.get('geocoding')]

        self.locations.append((self.activity.get_identifier(),
                               [data['geocoding'] for (l, data) in self.results if data.get('geocoding')]))
        return self

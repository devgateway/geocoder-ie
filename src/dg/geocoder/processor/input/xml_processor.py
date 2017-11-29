import logging.config

from dg.geocoder.config import get_log_config_path
from dg.geocoder.iati.activities_reader import ActivitiesParser
from dg.geocoder.iati.iati_validator import is_valid_schema
from dg.geocoder.processor.input.activity_processor import ActivityProcessor

logging.config.fileConfig(get_log_config_path())
logger = logging.getLogger()


class XMLProcessor:
    def __init__(self, file):
        self.file = file
        self.locations = []
        self.results = []

    def process(self):
        if not is_valid_schema(self.file, version='202'):
            logger.error('Invalid xml file supplied please check IATI version should be 202')
            raise Exception("Invalid xml file")
        else:
            parser = ActivitiesParser(self.file)
            for activity in parser.get_activities():
                activity_processor = ActivityProcessor(activity)
                activity_processor.process()
                self.locations = self.locations + activity_processor.get_locations()
                self.results = self.results + activity_processor.get_results()

    def get_locations(self):
        return self.locations

    def get_results(self):
        return self.results

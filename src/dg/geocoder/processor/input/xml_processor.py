import logging.config
import os

from dg.geocoder.config import get_log_config_path
from dg.geocoder.iati.activities_reader import ActivitiesParser
from dg.geocoder.iati.iati_validator import is_valid_schema
from dg.geocoder.processor.input.activity_processor import ActivityProcessor
from dg.geocoder.processor.input.base_processor import BaseProcessor, FORMAT_XML

logging.config.fileConfig(get_log_config_path())
logger = logging.getLogger()


class XMLProcessor(BaseProcessor):
    def __init__(self, file, **kwargs):
        BaseProcessor.__init__(self, file, **kwargs)
        self.file = file

    def process(self):
        if not is_valid_schema(self.file, version='202'):
            logger.error('Invalid xml file supplied please check IATI version should be 202')
            raise Exception("Invalid xml file")
        else:
            self.parser = ActivitiesParser(self.file)
            for activity in self.parser.get_activities():
                activity_processor = ActivityProcessor(activity)
                activity_processor.process()
                self.locations = self.locations + activity_processor.get_locations()
                self.results = self.results + activity_processor.get_results()
        return self

    def write_output(self, out_format=FORMAT_XML, out_path='', out_file='out'):
        if out_format == FORMAT_XML or out_format is None:
            out_file_with_extension = "{}.xml".format(out_file)
            self.parser.save(os.path.realpath(os.path.join(out_path, out_file_with_extension)))
            return out_file_with_extension
        else:
            return super().write_output(out_format=out_format, out_path=out_path, out_file=out_file)
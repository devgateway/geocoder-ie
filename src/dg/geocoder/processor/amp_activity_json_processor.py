import logging

from dg.geocoder.iati.json_activities_reader import JsonActivityParser
from dg.geocoder.processor.amp_activity_processor import AmpActivityProcessor
from dg.geocoder.processor.base_processor import BaseProcessor

logger = logging.getLogger()


class AmpActivityJsonProcessor(BaseProcessor):

    def __init__(self, file, **kwargs):
        BaseProcessor.__init__(self, file, **kwargs)
        self.file = file

    def process(self):
        self.parser = JsonActivityParser(self.file)
        for activity in self.parser.get_activities():
            activity_processor = AmpActivityProcessor(activity, step_logger=self.step_logger)
            activity_processor.process()
            self.locations = self.locations + activity_processor.get_locations()
            self.results = self.results + activity_processor.get_results()
        return self

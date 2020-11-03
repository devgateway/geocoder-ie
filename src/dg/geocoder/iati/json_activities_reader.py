import json
import logging

from dg.geocoder.readers.amp_json_reader import AmpJsonReader

logger = logging.getLogger()


def read_activity():
    logger.info('parse json activity')


class JsonActivityParser:
    def __init__(self, path=None):
        if path is not None:
            self.activity = json.load(open(path, 'r', encoding="UTF-8"))

    def get_activities(self):
        yield AmpJsonReader(self.activity)

    def save(self, name):
        json.dumps(self.activity)

from lxml import etree

from dg.geocoder.iati.activity_reader import ActivityReader
from dg.geocoder.iati.iati_validator import is_valid_schema, ValidationError


def read_activities():
    print('parse activity lists')


class ActivitiesReader:
    def __init__(self, path=None):
        if path is not None:
            if not is_valid_schema(path):
                raise ValidationError("Invalid xml file")
            self.root = etree.parse(path).getroot()

    def get_activities(self):
        for activity in self.root.findall('iati-activity'):
            yield ActivityReader(root=activity)

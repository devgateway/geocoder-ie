import logging

from lxml import etree

from dg.geocoder.iati.activity_reader import ActivityReader
from dg.geocoder.iati.iati_validator import is_valid_schema, ValidationError

logger = logging.getLogger()


def read_activities():
    logger.info('parse activity lists')


class ActivitiesReader:
    def __init__(self, path=None):
        if path is not None:
            if not is_valid_schema(path):
                raise ValidationError("Invalid xml file")
            self.root = etree.parse(path).getroot()

    def get_activities(self):
        for activity in self.root.findall('iati-activity'):
            yield ActivityReader(root=activity)

    def __str__(self):
        return etree.tostring(self.root).decode('utf-8')

    def xml(self):
        return self.__str__()

    def save(self, name):
        tree = etree.ElementTree(self.root)
        tree.write(name, pretty_print=True, xml_declaration=True, encoding="utf-8")

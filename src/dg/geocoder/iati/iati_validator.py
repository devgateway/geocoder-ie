from lxml import etree

from dg.geocoder.config import get_activities_xsd_file_path


def is_valid_schema(xml_path, version='202'):
    xsd_path = get_activities_xsd_file_path(version)
    xmlschema_doc = etree.parse(xsd_path)
    xmlschema = etree.XMLSchema(xmlschema_doc)

    xml_doc = etree.parse(xml_path)
    return xmlschema.validate(xml_doc)


class ValidationError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)

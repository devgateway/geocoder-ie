import urllib
import xml.etree.ElementTree as ET

from dg.geocoder.iati.iati_codes import iati_regions, iati_countries, iati_publishers


def read_activities():
    print('parse activity lists')


class ActivityReader:
    def __init__(self, path=None, root=None):
        if path is not None:
            self.root = ET.parse(urllib.urlopen(path)).getroot()
        elif root is not None:
            self.root = root

    def get_identifier(self):
        return self.root.find('iati-identifier').text

    def get_recipient_region_code(self):
        recipient_region_code = self.root.find('recipient-region')
        if recipient_region_code is not None:
            return recipient_region_code.get('code')
        return None

    def get_recipient_region_name(self):
        return iati_regions[
            int(self.get_recipient_region_code())] if self.get_recipient_region_code() is not None else None

    def get_recipient_country_code(self):
        recipient_country = self.root.find('recipient-country')
        if recipient_country is not None:
            return recipient_country.get('code')
        return None

    def get_recipient_country_name(self):
        return iati_countries[
            self.get_recipient_country_code()] if self.get_recipient_country_code() is not None else None

    def get_reporting_organisation_code(self):
        element = self.root.find('reporting-org')
        if element is not None:
            return element.get('ref')
        return None

    def get_reporting_organisation_name(self):
        return iati_publishers[self.get_reporting_organisation_code()]

    def get_document_links(self):
        return [(doc) for doc in self.root.findall("document-link") if
                len(doc.findall("category[@code='A02']")) > 0 or len(doc.findall("category[@code='A07']")) > 0]

    def has_documents(self):
        return len(self.root.findall("document-link/category[@code='A02']") + self.root.findall(
            "document-link/category[@code='A07']")) > 0

    def getXML(self):
        return ET.tostring(self.root)

    def save(self):
        print('Save activity in database')

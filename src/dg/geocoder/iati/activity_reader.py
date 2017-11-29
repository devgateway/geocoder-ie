import logging
from io import StringIO
from lxml import etree as et

from dg.geocoder.iati.iati_codes import iati_regions, iati_countries

logger = logging.getLogger()


class ActivityReader:
    def __init__(self, path=None, root=None, xml=None):
        if path is not None:
            self.root = et.parse(path).getroot()
        elif root is not None:
            self.root = root
        elif xml is not None:
            self.root = et.parse(StringIO(xml)).getroot()

    def get_identifier(self):
        return self.root.find('iati-identifier').text

    def get_texts(self):
        texts = []
        [[texts.append(item.text) for item in el if item.text is not None] for el in self.root if
         el.tag in {'title', 'description'}]
        return texts

    def get_recipient_region_code(self):
        recipient_region_code = self.root.find('recipient-region')
        if recipient_region_code is not None:
            return recipient_region_code.get('code')
        return None

    def get_title(self):
        title = self.root.find('title')[0]
        if title is not None:
            return title.text
        return None

    def get_description(self):
        description = self.root.find('description')[0]
        if description is not None:
            return description.text
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
        element = self.root.find('reporting-org')
        if element is not None:
            if element.find('narrative') is not None:
                return element.find('narrative').text
            elif element.text is not None:
                return element.text
            else:
                return self.get_reporting_organisation_code()
        else:
            return None

    def get_document_links(self):
        return [doc for doc in self.root.findall("document-link") if
                len(doc.findall("category[@code='A02']")) > 0 or len(doc.findall("category[@code='A07']")) > 0]

    def has_documents(self):
        return len(self.root.findall("document-link/category[@code='A02']") + self.root.findall(
            "document-link/category[@code='A07']")) > 0

    def __str__(self):
        return et.tostring(self.root).decode('utf-8')

    def xml(self):
        return self.__str__()

    def add_location(self, loc_data):
        location = et.SubElement(self.root, "location")
        et.SubElement(location, "location-reach", code="1")
        et.SubElement(location, "location-id", vocabulary='G1', code=str(loc_data['geonameId']))
        et.SubElement(et.SubElement(location, "name"), "narrative").text = loc_data['name']
        et.SubElement(et.SubElement(location, "description"), "narrative").text = loc_data['fcodeName']
        # activity = ''
        # if texts:
        #    activity = '\n'.join([t['text'] for t in texts])

        # logger.info(activity)
        # ET.SubElement(ET.SubElement(location, "activity-description"), "narrative").text = activity

        et.SubElement(location, "administrative",
                      vocabulary="G1", level=loc_data['fcode'], code=str(loc_data['geonameId']))

        et.SubElement(et.SubElement(location, "point"), "pos").text = "{} {}".format(
            str(loc_data['lat']), str(loc_data['lng']))

        et.SubElement(location, "exactness", code="1")
        et.SubElement(location, "location-class", code="2")
        et.SubElement(location, "feature-designation", code=loc_data['fcode'])

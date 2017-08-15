from lxml import etree as ET

from dg.geocoder.iati.iati_codes import iati_regions, iati_countries, iati_publishers


def read_activities():
    print('parse activity lists')


class ActivityReader:
    def __init__(self, path=None, root=None):
        if path is not None:
            self.root = ET.parse(path).getroot()
        elif root is not None:
            self.root = root

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

    def __str__(self):
        return ET.tostring(self.root).decode('utf-8')

    def xml(self):
        return self.__str__()

    def add_location(self, loc_data, texts):
        location = ET.SubElement(self.root, "location")
        ET.SubElement(location, "location-reach", code="1")
        ET.SubElement(location, "location-id", vocabulary='G1', code=str(loc_data['geonameId']))
        ET.SubElement(ET.SubElement(location, "name"), "narrative").text = loc_data['name']
        ET.SubElement(ET.SubElement(location, "description"), "narrative").text = loc_data['fcodeName']
        # activity = ''
        # if texts:
        #    activity = '\n'.join([t['text'] for t in texts])

        # print(activity)
        # ET.SubElement(ET.SubElement(location, "activity-description"), "narrative").text = activity

        ET.SubElement(location, "administrative",
                      vocabulary="G1", level=loc_data['fcode'], code=str(loc_data['geonameId']))

        location_pos = ET.SubElement(ET.SubElement(location, "point"), "pos").text = "{} {}".format(
            str(loc_data['lat']), str(loc_data['lng']))

        ET.SubElement(location, "exactness", code="1")
        ET.SubElement(location, "location-class", code="2")
        ET.SubElement(location, "feature-designation", code=loc_data['fcode'])

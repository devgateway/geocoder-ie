import unittest

from dg.geocoder.geo.geocoder import geocode, merge, extract, join, geonames
from dg.geocoder.processor import process_xml, process
from dg.geocoder.readers.factory import get_text_reader, get_reader


class TestGeocoder(unittest.TestCase):
    def test_geocode_string(self):
        text = """The project aims to improve the road connections om the North-West Fouta Djallon area.
                In order to further support this political will towards poverty reduction, the
                African Development Bank (ADB) granted the Guinean Government’s request for the
                financing of the preparation of the feasibility study on a rural development support project in
                the North-West Fouta Djallon area, in particular Gaoual and Koundara prefectures in the
                
                Middle Guinea region."""

        geo = geocode([text], [], ['GN'])
        print('Checking Koundara as ADM2')
        Koundara = [(data) for loc, data in geo if loc == 'Koundara'][0]
        self.assertTrue(Koundara.get('geocoding').get('fcode') == 'ADM2')
        print('Checking Gaoual as ADM2')
        Gaoual = [(data) for loc, data in geo if loc == 'Gaoual'][0]
        self.assertTrue(Gaoual.get('geocoding').get('fcode') == 'ADM2')
        print('Checking  Fouta Djallon  as ADM2')
        Fouta_Djallon = [(data) for loc, data in geo if loc == 'Fouta Djallon'][0]
        self.assertTrue(Fouta_Djallon.get('geocoding').get('fcode') == 'RGN')

    def test_geocode_txt_2(self):
        text = get_reader('resources/sample_text_2.txt').split()[0]
        ner_decorated = extract(get_text_reader(text).split())
        merge_decorated = merge(ner_decorated)
        normalized = join(merge_decorated)
        found = [l for l, data in normalized]
        self.assertTrue('Benin' in found)
        self.assertTrue('Ghana' in found)
        self.assertTrue('Mozambique' in found)
        self.assertTrue('Burkina Faso' in found)

        geonames_decorated = geonames(normalized, cty_codes=['BF'])
        locs = [(l) for (l, data) in geonames_decorated if data.get('geocoding')]
        self.assertFalse('Benin' in locs)
        self.assertFalse('Ghana' in locs)
        self.assertFalse('Mozambique' in locs)
        self.assertTrue('Burkina Faso' in locs)

        # geocode without country filter
        geonames_decorated2 = geonames(join(merge_decorated))
        locs = [(l) for (l, data) in geonames_decorated2 if data.get('geocoding')]

        self.assertTrue('Benin' in locs)
        self.assertTrue('Ghana' in locs)
        self.assertTrue('Mozambique' in locs)
        self.assertTrue('Burkina Faso' in locs)

    def test_afdb_sub_national(self):
        geo = geocode([], ['resources/afdb_subnational.pdf'], ['GN'])
        locs = [(l) for (l, data) in geo if data.get('geocoding')]
        self.assertTrue('Guinea' in locs)
        self.assertTrue('Conakry' in locs)
        self.assertTrue('Koundara' in locs)
        self.assertTrue('GUINEA' in locs)
        self.assertTrue('Fouta Djallon' in locs)
        self.assertTrue('Republic of Guinea' in locs)
        self.assertTrue('Gaoual' in locs)

    def test_geocode_text_3(self):
        geo = geocode([], ['resources/sample_text_3.txt'], [])
        locs = [(l) for (l, data) in geo if data.get('geocoding')]

    def test_afdb_activities_XML(self):
        process_xml('resources/afdb_3_activities.xml')

    def test_afdb_activities_XML_1(self):
        process_xml('resources/afdb_1_no_docs_activities.xml')

    def test_dfid_simple_document(self):
        process('resources/dfid_4182791.odt',None)


if __name__ == '__main__':
    unittest.main()

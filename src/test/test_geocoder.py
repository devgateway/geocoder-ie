import unittest

from dg.geocoder.config import get_download_path
from dg.geocoder.geo.geocoder import geocode, merge
from dg.geocoder.iati.activities_reader import ActivitiesReader
from dg.geocoder.iati.iati_downloader import download_activity_data
from dg.geocoder.iati.iati_validator import is_valid_schema


class TestGeocoder(unittest.TestCase):
    def test_geocode_1(self):
        text = """The project aims to improve the road connections om the North-West Fouta Djallon area.
                
                In order to further support this political will towards poverty reduction, the
                African Development Bank (ADB) granted the Guinean Government’s request for the
                financing of the preparation of the feasibility study on a rural development support project in
                the North-West Fouta Djallon area, in particular Gaoual and Koundara prefectures in the
                
                Middle Guinea region."""

        geo = geocode(text=text, country_codes=['GN'])
        print('Checking Koundara as ADM2')
        Koundara = [(data) for loc, data in geo if loc == 'Koundara'][0]
        self.assertTrue(Koundara.get('geocoding').get('fcode') == 'ADM2')
        print('Checking Gaoual as ADM2')
        Gaoual = [(data) for loc, data in geo if loc == 'Gaoual'][0]
        self.assertTrue(Gaoual.get('geocoding').get('fcode') == 'ADM2')
        print('Checking  Fouta Djallon  as ADM2')
        Fouta_Djallon = [(data) for loc, data in geo if loc == 'Fouta Djallon'][0]
        self.assertTrue(Fouta_Djallon.get('geocoding').get('fcode') == 'RGN')

    def test_geocode_2(self):
        text = """The project aims to improve the road connections (Cordoba, Catamarca ,Santiago del Estero, Villa Allende, Mendiolaza, Unquillo in sierras chias) to serve large numbers of poor people in these adjacent 
                             areas"""
        geo = geocode(text=text, country_codes=['AR'])

        print('Checking  Mendiolaza as PPL')
        Mendiolaza = [(data) for loc, data in geo if loc == 'Mendiolaza'][0]
        self.assertTrue(Mendiolaza.get('geocoding').get('fcode') == 'PPL')

    def test_geocode_3(self):
        text = """The project aims to improve the road connections (Cordoba, Catamarca ,Santiago del Estero, Villa Allende, Mendiolaza, Unquillo in sierras chias) to serve large numbers of poor people in these adjacent 
                             areas"""
        geo = geocode(text=text, country_codes=['AR'])

    def test_merge(self):
        text = "Congo,New Guinea and Burkina Faso, same as the route Cordoba-Catamarca, Democratic Republic of Congo"
        entities = ['Congo', 'New', 'Guinea', 'Burkina Faso', 'Cordoba', 'Catamarca', 'Democratic', 'Republic', 'of',
                    'Congo']
        rels = []
        extraction = []
        extraction.append(({'text': text, 'entities': entities, 'relations': []}))
        results = merge(extraction)
        self.assertTrue('New Guinea' in results[0]['locations'])
        self.assertTrue('Cordoba' in results[0]['locations'])
        self.assertTrue('Burkina Faso' in results[0]['locations'])
        self.assertTrue('Democratic Republic of Congo' in results[0]['locations'])

    def test_geocode_document(self):
        geo = geocode(file='1.pdf', country_codes=['GN'])
        locs = [(l) for (l, data) in geo if data.get('geocoding')]
        self.assertTrue('Guinea' in locs)
        self.assertTrue('Conakry' in locs)
        self.assertTrue('Koundara' in locs)
        self.assertTrue('UPPER GUINEA' in locs)
        self.assertTrue('Fouta Djallon' in locs)
        self.assertTrue('Republic of Guinea' in locs)
        self.assertTrue('Gaoual' in locs)

    def test_geocode_activities_XML(self):
        self.assertTrue(is_valid_schema('afdb_ag_activities.xml', version='202'))
        reader = ActivitiesReader('afdb_ag_activities.xml')
        activities = reader.get_activities()
        for activity in activities:
            documents = download_activity_data(activity, get_download_path())
            ##geo = geocode(file='1.pdf', country_codes=['GN'])
            print(documents)


if __name__ == '__main__':
    unittest.main()

import unittest

from dg.geocoder.config import get_download_path
from dg.geocoder.geo.geocoder import geocode, merge, extract, join, geonames
from dg.geocoder.iati.activities_reader import ActivitiesReader
from dg.geocoder.iati.iati_downloader import download_activity_data
from dg.geocoder.iati.iati_validator import is_valid_schema
from dg.geocoder.readers.factory import get_text_reader


class TestGeocoder(unittest.TestCase):
    def test_geocode_1(self):
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

    def tes_text_numbers(self):
        text = """The project aims to improve the road connections (Cordoba, Catamarca ,Santiago del Estero, Villa Allende, Mendiolaza, Unquillo in sierras chias) to serve large numbers of poor people in these adjacent 
                             areas"""
        geo = geocode([text], [], country_codes=['BK'])
        self.assertTrue(True)
        print(geo)

    def test_geocode_3(self):
        text = """The project aims to improve the road connections (Cordoba, Catamarca ,Santiago del Estero, Villa Allende, Mendiolaza, Unquillo in sierras chias) to serve large numbers of poor people in these adjacent 
                             areas"""
        geo = geocode(text=text, country_codes=['AR'])

    def test_merge_2(self):
        text = """ 2,509,000,000 
            
            2016-2019 
            
            Contribute to the development of tuber roots value 
            chains 
            
            98,700,000 
            
            2014-2019 
            
            Help to increase Burkina Faso’s sesame exports  
            
             
            
             
            
            20 
            
            Sustainable Development 
            Support Project Phase II 
            
            (PADD II) 
            
            21 
            
            Project for Restoration of 
            
            Classified Forests of Wayen 
            
            and Bissiga in Central 
            Plateau Region (PRBW 
            Project to support the 
            
            22 
            
            1,817,200,000 
            
            development of Oleo-protein 
            
            3,291,400,000 
            
            value chains 
            
            23 
            
            Support Project for the 
            
            Development of Tuber Roots 
            
            2,509,000,000 
            
            Value Chain 
            
            24 
            
            Sesame production 
            
            Strengthening Project 
            
            1,204,890,000 
            
            25 
            
            Rice Sector Structuring 
            
            Support Project 
            
            225,000,000 
            
            26 
            
            Maize Sector Structuring 
            
            Support Project 
            
            300,000,000 
            
            JICA (Japan 
            International 
            Cooperation  
            
            Agency)  
            
            1,106,190,000 
            
            WAEMU  
            225,000,000 
            
            WAEMU 
            
            300,000,000 
            
            0 
            
            0 
            
            0 
            
            2015-2017 
            
            2015-2017 
            
            2015-2018 
            
            Contribute to the development of the rice sector in 
            order  to  sustainably  improve  its  contribution  to 
            food security and poverty reduction.
            """
        entities = extract(get_text_reader(text).split())
        for l in merge(entities)[0]['locations']:
            print(l)

    def test_merge_3(self):
        text = """ 27
    
        Capacity building and
    
        experience-sharing project
        for sustainable development
    
        of the rice value chain
        through South-South
    
        cooperation
    
        28
    
        Nut Shelling Project for 2
    
        countries, Benin and
    
        300,000,000
    
        300,000,000
    
        Burkina Faso
    
        2,875,000,000
    
        NA
    
        65,600,000
    
        2016-2021
    
        29
    
        ComCashew project for 5
        countries namely, Benin,
    
        Burkina Faso,  Côte
        d’Ivoire, Ghana and
    
        Mozambique
    
    
    
    
        6,000,000,000
    
        NA
    
        600,000,000
    
        2016-2018


    
        VII"""

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
        geo = geocode([], ['1.pdf'], ['GN'])
        locs = [(l) for (l, data) in geo if data.get('geocoding')]
        self.assertTrue('Guinea' in locs)
        self.assertTrue('Conakry' in locs)
        self.assertTrue('Koundara' in locs)
        self.assertTrue('GUINEA' in locs)
        self.assertTrue('Fouta Djallon' in locs)
        self.assertTrue('Republic of Guinea' in locs)
        self.assertTrue('Gaoual' in locs)

    def test_geocode_documen_2(self):
        geo = geocode([], ['2.pdf'], ['BK'])
        locs = [(l) for (l, data) in geo if data.get('geocoding')]
        print(locs)

    def test_geocode_activities_XML(self):
        self.assertTrue(is_valid_schema('afdb_ag_activities.xml', version='202'))
        reader = ActivitiesReader('afdb_ag_activities.xml')
        activities = reader.get_activities()
        for activity in activities:
            documents = download_activity_data(activity, get_download_path())
            texts = activity.get_texts()
            results = geocode(texts, documents, cty_codes=[activity.get_recipient_country_code()])
            locs = [(l) for (l, data) in results if data.get('geocoding')]

if __name__ == '__main__':
    unittest.main()

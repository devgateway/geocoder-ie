from dg.geocoder.config import get_download_path
from dg.geocoder.geo.geocoder import geocode
from dg.geocoder.iati.activities_reader import ActivitiesReader
from dg.geocoder.iati.iati_downloader import download_activity_data
from dg.geocoder.iati.iati_validator import is_valid_schema
from dg.geocoder.util.file_util import is_xml


def process_xml(file, xml_name='out.xml', persist=False):
    if not is_valid_schema(file, version='202'):
        print('Invalid xml file supplied please check IATI standard ')
    else:
        reader = ActivitiesReader(file)
        activities = reader.get_activities()
        for activity in activities:
            print('.......... Coding activity {} ..........'.format(activity.get_identifier()))
            # Get activity related documents
            documents = download_activity_data(activity, get_download_path())
            # extract title and descriptions a
            texts = activity.get_texts()
            # call full geocode workflow
            # TODO CHECK if country code can be an array
            # full results
            results = geocode(texts, documents, cty_codes=[activity.get_recipient_country_code()])
            [activity.add_location(data['geocoding'], data['texts']) for (l, data) in results if data.get('geocoding')]

        reader.save(xml_name)
        print('File {} saved '.format(xml_name))


def process(file):
    if is_xml(file):
        process_xml(file)

from dg.geocoder.config import get_download_path
from dg.geocoder.geo.geocoder import geocode
from dg.geocoder.iati.activities_reader import ActivitiesReader
from dg.geocoder.iati.iati_downloader import download_activity_data
from dg.geocoder.iati.iati_validator import is_valid_schema


def process_xml(file, to_xml=False, persist=False):
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
            # geocoded location only
            geocoded = [(l) for (l, data) in results if data.get('geocoding')]
            print(geocoded)


            # if persist:
            #    persist(results)
            # if to_xml:
            #    print('Update xml tree')
            #    pass
            # xml_output(reader,results)
            # else:
            #    console_output()





def process_files(files, persist=False):
    results = geocode([], files)


def console_output():
    pass


def xml_output():
    pass


def persit():
    pass

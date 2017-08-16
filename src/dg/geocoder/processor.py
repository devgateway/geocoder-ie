import os

from dg.geocoder.config import get_download_path
from dg.geocoder.geo.geocoder import geocode
from dg.geocoder.iati.activities_reader import ActivitiesReader
from dg.geocoder.iati.iati_downloader import download_activity_data
from dg.geocoder.iati.iati_validator import is_valid_schema
from dg.geocoder.util.file_util import is_xml, is_valid


def process_xml(file, out_put_name='out.xml', persist=False, path_to_docs=''):
    if not is_valid_schema(file, version='202'):
        print('Invalid xml file supplied please check IATI standard ')
        return None
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

            reader.save(os.path.realpath(os.path.join(path_to_docs, out_put_name)))
            # if persist:
            # call persit geocoder
            # save in db
        print('File {} saved '.format(out_put_name))
        return out_put_name


def process_document(document, out_put_name='out.csv', cty_codes=[]):
    results = geocode([], [document], cty_codes=[])


def persist_db():
    pass


def process_queue():
    # read pending
    # iterates
    #   if xml process_xml persit=true
    #   if odc process doc persit=true
    # update queue status done
    pass


def process(file):
    if not is_valid(file):
        print('Not valid file provided')
        return None
    else:
        if is_xml(file):
            process_xml(file)
        else:
            process_document(file)

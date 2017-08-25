import csv
import os

from dg.geocoder.config import get_download_path, get_doc_queue_path
from dg.geocoder.geo.geocoder import geocode
from dg.geocoder.iati.activities_reader import ActivitiesReader
from dg.geocoder.iati.iati_downloader import download_activity_data
from dg.geocoder.iati.iati_validator import is_valid_schema
from dg.geocoder.util.file_util import is_xml, is_valid
from dg.geocoder.db.geocode import save_geocoding, save_extract_text, save_activity
from dg.geocoder.db.doc_queue import get_docs, update_doc, get_document_by_id


def process_xml(file, out_file='out.xml', persist=False, path_to_docs='', doc_id=None):
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

            if persist:
                identifier = activity.get_identifier()
                title = activity.get_title()
                description = activity.get_description()
                country = activity.get_recipient_country_code()
                activity_id = save_activity(identifier, title, description, country, doc_id)
                geocoding = [(data['geocoding'], data['texts']) for (l, data) in results if data.get('geocoding')]
                persist_geocoding(geocoding, doc_id, activity_id)

        reader.save(os.path.realpath(os.path.join(path_to_docs, out_file)))
        print('File {} saved '.format(out_file))
        return out_file


def process_document(document, out_file='out.tsv', cty_codes=[], persist=False, path_to_docs='', doc_id=None):
    results = geocode([], [document], cty_codes=cty_codes)

    geocoding = [(data['geocoding'], data['texts']) for (l, data) in results if data.get('geocoding')]
    if persist:
        persist_geocoding(geocoding, doc_id, None)

    with open(os.path.realpath(os.path.join(path_to_docs, out_file)), 'w+', newline='') as csvfile:
        fieldnames = ['geonameId', 'name', 'toponymName', 'fcl', 'fcode', 'fcodeName', 'fclName', 'lat', 'lng',
                      'adminCode1', 'adminName1', 'adminCode2', 'adminName2', 'adminCode3', 'adminName3', 'adminCode4',
                      'adminName4', 'countryName', 'population', 'continentCode', 'countryCode',
                      ]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter='\t', quotechar='"',
                                quoting=csv.QUOTE_MINIMAL)
        writer.writeheader()
        for data, text in geocoding:
            writer.writerow(data)
    csvfile.close()

    return out_file


def process_queue():
    pending_docs = get_docs(1, 10, 'PENDING').get('rows')
    for doc in pending_docs:
        doc_id = doc[0]
        doc_name = doc[1]
        doc_type = doc[2]
        doc_country_code = doc[6]
        update_doc(doc_id, 'PROCESSING')
        if doc_type == 'text/xml':
            process_xml(get_doc_queue_path()+"""\\"""+doc_name, doc_name.split('.')[0]+"""_out.xml""", True,
                        get_doc_queue_path()+"""\\""", doc_id)
        else:
            process_document(get_doc_queue_path()+"""\\"""+doc_name, doc_name.split('.')[0]+"""_out.tsv""",
                             [doc_country_code], True, get_doc_queue_path()+"""\\""", doc_id)
        update_doc(doc_id, 'PROCESSED')
    return None


def process_doc(doc_id):
    doc = get_document_by_id(doc_id)
    doc_id = doc[0]
    doc_name = doc[1]
    doc_type = doc[2]
    doc_country_code = doc[6]
    update_doc(doc_id, 'PROCESSING')
    if doc_type == 'text/xml':
        process_xml(get_doc_queue_path()+"""\\"""+doc_name, doc_name.split('.')[0]+"""_out.xml""", True,
                    get_doc_queue_path()+"""\\""", doc_id)
    else:
        process_document(get_doc_queue_path()+"""\\"""+doc_name, doc_name.split('.')[0]+"""_out.tsv""",
                         [doc_country_code], True, get_doc_queue_path()+"""\\""", doc_id)
    update_doc(doc_id, 'PROCESSED')
    return None


def process(file, cty_codes=[]):
    if not is_valid(file):
        print('Not valid file provided')
        return None
    else:
        if is_xml(file):
            return process_xml(file)
        else:
            return process_document(file, cty_codes=cty_codes)


def persist_geocoding(geocoding_list, doc_id, activity_id):
    for geocoding in geocoding_list:
        geo_id = save_geocoding(geocoding[0], doc_id, activity_id)
        for text in geocoding[1]:
            save_extract_text(text.get('text'), geo_id, ', '.join(text.get('entities'))	)
    return None

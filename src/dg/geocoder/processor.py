import csv
import logging.config
import os

from dg.geocoder.config import get_download_path, get_doc_queue_path, get_log_config_path
from dg.geocoder.db.doc_queue import get_docs, update_doc_status, get_document_by_id
from dg.geocoder.db.geocode import save_geocoding, save_extract_text, save_activity
from dg.geocoder.geo.geocoder import geocode
from dg.geocoder.iati.activities_reader import ActivitiesReader
from dg.geocoder.iati.iati_downloader import download_activity_data
from dg.geocoder.iati.iati_validator import is_valid_schema
from dg.geocoder.util.file_util import is_xml, is_valid

ST_PROCESSING = "PROCESSING"
ST_PROCESSED = "PROCESSED"
ST_PENDING = "PENDING"
ST_ERROR = "ERROR"

logging.config.fileConfig(get_log_config_path())
logger = logging.getLogger()


# DB processors

def process_by_id(doc_id):
    logger.info('Getting doc record')
    doc = get_document_by_id(doc_id)
    _process_doc(doc)


def process_queue():
    pending_docs = get_docs(1, 10, ST_PENDING).get('rows')
    for doc in pending_docs:
        _process_doc(doc)


# File processor
def process_file(file, cty_codes=None):
    if cty_codes is None:
        cty_codes = []
    if not is_valid(file):
        logger.info('Not valid file provided')
        return None
    else:
        if is_xml(file):
            return process_xml(file)
        else:
            return process_document(file, cty_codes=cty_codes)


def _process_doc(doc):
    logger.info('processing doc {}'.format(doc[0]))
    doc_id = doc[0]
    doc_name = doc[1]
    doc_type = doc[2]
    doc_country_code = doc[6]
    update_doc_status(doc_id, ST_PROCESSING)

    try:
        if doc_type == 'text/xml':
            process_xml(os.path.join(get_doc_queue_path(), doc_name),
                        out_file="{}_out.xml".format(doc_name.split('.')[0]),
                        persist=True,
                        doc_id=doc_id)

        else:
            process_document(os.path.join(get_doc_queue_path(), doc_name),
                             out_file="{}_out.tsv".format(doc_name.split('.')[0]),
                             cty_codes=[doc_country_code],
                             persist=True,
                             doc_id=doc_id)

        update_doc_status(doc_id, ST_PROCESSED)
    except Exception as error:
        logger.info("Oops!  something didn't go well", error)
        update_doc_status(doc_id, ST_ERROR, message=error.__str__())


def process_xml(file, out_file='out.xml', persist=False, doc_id=None):
    if not is_valid_schema(file, version='202'):
        logger.error('Invalid xml file supplied please check IATI standard')
        raise Exception("Invalid xml file")
    else:
        reader = ActivitiesReader(file)
        activities = reader.get_activities()
        for activity in activities:
            logger.info('.......... Coding activity {} ..........'.format(activity.get_identifier()))

            # Get activity related documents
            documents = download_activity_data(activity, get_download_path())
            # extract title and descriptions a
            texts = activity.get_texts()
            # call full geocode workflow
            # TODO CHECK if country code can be an array
            # full results
            results = geocode(texts, documents, cty_codes=[activity.get_recipient_country_code()])
            [activity.add_location(data['geocoding']) for (l, data) in results if data.get('geocoding')]

            if persist:
                _persist_activity(results, activity, doc_id)

        reader.save(os.path.realpath(out_file))
        logger.info('File {} saved '.format(out_file))
        return out_file


def process_document(document, out_file='out.tsv', cty_codes=None, persist=False, doc_id=None, tracer=None):
    if cty_codes is None:
        cty_codes = []
    results = geocode([], [document], cty_codes=cty_codes, tracer=tracer)
    geocoding = [(data['geocoding'], data['texts']) for (l, data) in results if data.get('geocoding')]

    # save results to db
    if persist:
        _persist_geocoding(geocoding, doc_id, None)

    # save results to disk
    return _save_to_tsv(out_file, geocoding)


def _save_to_tsv(out_file, geocoding):
    try:
        with open(os.path.realpath(os.path.join(out_file)), 'w+', newline='') as csvfile:
            fieldnames = ['geonameId', 'name', 'toponymName', 'fcl', 'fcode', 'fcodeName', 'fclName', 'lat', 'lng',
                          'adminCode1', 'adminName1', 'adminCode2', 'adminName2', 'adminCode3', 'adminName3',
                          'adminCode4',
                          'adminName4', 'countryName', 'population', 'continentCode', 'countryCode',
                          ]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter='\t', quotechar='"',
                                    quoting=csv.QUOTE_MINIMAL)
            writer.writeheader()
            for data, text in geocoding:
                writer.writerow(data)
        csvfile.close()
        return out_file
    except:
        raise


def _persist_activity(results, activity, doc_id):
    identifier = activity.get_identifier()
    title = activity.get_title()
    description = activity.get_description()
    country = activity.get_recipient_country_code()
    activity_id = save_activity(identifier, title, description, country, doc_id)
    geocoding = [(data['geocoding'], data['texts']) for (l, data) in results if data.get('geocoding')]
    _persist_geocoding(geocoding, doc_id, activity_id)


def _persist_geocoding(geocoding_list, doc_id, activity_id):
    for geocoding in geocoding_list:
        geo_id = save_geocoding(geocoding[0], doc_id, activity_id)
        for text in geocoding[1]:
            save_extract_text(text.get('text'), geo_id, ', '.join(text.get('entities')))
    return None

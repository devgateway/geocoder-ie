import csv
import json
import logging.config
import os

from dg.geocoder.config import get_download_path, get_doc_queue_path, get_log_config_path
from dg.geocoder.db.doc_queue import get_docs, update_doc_status, get_document_by_id
from dg.geocoder.db.geocode import save_geocoding, save_extract_text, save_activity
from dg.geocoder.geo.geocoder import geocode
from dg.geocoder.iati.activities_reader import ActivitiesReader
from dg.geocoder.iati.iati_downloader import download_activity_data
from dg.geocoder.iati.iati_validator import is_valid_schema
from dg.geocoder.model.models import get_activity_dict, get_location_dic
from dg.geocoder.util.file_util import is_xml, is_valid

ST_PROCESSING = "PROCESSING"
ST_PROCESSED = "PROCESSED"
ST_PENDING = "PENDING"
ST_ERROR = "ERROR"

logging.config.fileConfig(get_log_config_path())
logger = logging.getLogger()


# DB processors
def step_log(doc_id):
    def log(step):
        update_doc_status(doc_id, ST_PROCESSING, message=step)

    return log


def process_by_id(doc_id):
    logger.info('Getting doc record')
    doc = get_document_by_id(doc_id)
    process_doc(doc, out_path=get_doc_queue_path())


def process_queue():
    pending_docs = get_docs(1, 10, [ST_PENDING]).get('rows')
    for doc in pending_docs:
        process_doc(doc, out_path=get_doc_queue_path())


# Process any input file
def process_file(file, cty_codes=None, out_format='json'):
    if cty_codes is None:
        cty_codes = []
    if not is_valid(file):
        logger.info('Not valid file provided')
        return None
    else:
        if is_xml(file):
            return process_xml(file, out_format=out_format)
        else:
            return process_document(file, cty_codes=cty_codes, out_format=out_format)


# Process a database document record
def process_doc(doc, out_path=''):
    logger.info('processing doc {}'.format(doc.get('id')))
    doc_id = doc.get('id')
    doc_name = doc.get('file_name')
    doc_type = doc.get('type')
    doc_country_code = doc.get('country_iso')

    update_doc_status(doc_id, ST_PROCESSING)

    try:
        if doc_type == 'text/xml':
            process_xml(os.path.join(get_doc_queue_path(), doc_name),
                        out_file="{}_out.xml".format(doc_name.split('.')[0]),
                        out_format='xml',
                        persist=True,
                        doc_id=doc_id, step_log=step_log(doc_id), out_path=out_path, format='xml')

        else:
            process_document(os.path.join(get_doc_queue_path(), doc_name),
                             out_file="{}_out.{}.tsv".format(doc_name.split('.')[0], doc_name.split('.')[1]),
                             cty_codes=[doc_country_code],
                             out_format='tsv',
                             persist=True,
                             doc_id=doc_id, step_log=step_log(doc_id), out_path=out_path)

        update_doc_status(doc_id, ST_PROCESSED)
    except Exception as error:
        logger.info("Oops!  something didn't go well", error)
        update_doc_status(doc_id, ST_ERROR, message=error.__str__())


# Process document file
def process_document(document, out_file=None, cty_codes=None, persist=False, doc_id=None, step_log=None,
                     out_path='', out_format='json'):
    if out_file is None and out_format == 'tsv':
        out_file = 'out.tsv'
    elif out_file is None and out_format == 'json':
        out_file = 'out.json'

    if out_format == 'xml':
        logger.error('xml output is not supported when processing documents ')
        raise Exception("Invalid output format")
    else:

        if cty_codes is None:
            cty_codes = []
        results = geocode([], [document], cty_codes=cty_codes, step_log=step_log)
        geocoding = [(data['geocoding'], data['texts']) for (l, data) in results if data.get('geocoding')]
        # save results to db
        if persist:
            persist_geocoding(geocoding, doc_id, None)

        # save results to disk
        if out_format == 'json':
            return save_to_json(out_file, [(document, [a[0] for a in geocoding])], out_path)
        elif out_format == 'tsv':
            return save_to_tsv(out_file, geocoding, out_path)


# Process a IATI activities xml
def process_xml(file, out_file=None, persist=False, doc_id=None, step_log=None, out_path='', out_format='json'):
    if not is_valid_schema(file, version='202'):
        logger.error('Invalid xml file supplied please check IATI standard')
        raise Exception("Invalid xml file")
    elif out_format == 'tsv':
        logger.error('tsv output is not supported when processing xml files')
        raise Exception("Invalid output format")
    else:

        if out_file is None and out_format == 'json':
            out_file = 'out.json'
        elif out_file is None and out_format == 'xml':
            out_file = 'out.xml'

        locs = []
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
            results = geocode(texts, documents, cty_codes=[activity.get_recipient_country_code()], step_log=step_log)

            if out_format == 'xml':
                # add location to activity
                [activity.add_location(data['geocoding']) for (l, data) in results if data.get('geocoding')]
            elif out_format == 'json' or out_format == 'tsv':
                # collect location to print them as json
                locs.append((activity.get_identifier(),
                             [data['geocoding'] for (l, data) in results if data.get('geocoding')]))
            # persis current activity result in database o
            if persist:
                persist_activity(results, activity, doc_id)

        # save all results to geojson file
        if out_format == 'json':
            save_to_json(out_file, locs, out_path)

        return out_file


# Save results to TSV
def save_to_tsv(out_file, geocoding, out_path=''):
    try:
        with open(os.path.realpath(os.path.join(out_path, out_file)), 'w+', newline='') as csvfile:
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
    except Exception as e:
        logger.error('Error while writing tsv file {}'.format(e))
        raise


def save_to_json(out_file, activities_locations, out_path=''):
    try:
        json_data = []
        for id, locations in activities_locations:
            json_data.append(get_activity_dict(id, get_location_dic(locations)))

        with open(out_file, 'w') as f:
            json.dump(json_data, f, ensure_ascii=False, indent=4)

        f.close()
        return out_file
    except Exception as e:
        logger.error('Error while writing json file {}'.format(e))
        raise


def save_to_xml(out_file, activity_reader, out_path=''):
    activity_reader.save(os.path.realpath(os.path.join(out_path, out_file)))


def persist_activity(results, activity, doc_id):
    identifier = activity.get_identifier()
    title = activity.get_title()
    description = activity.get_description()
    country = activity.get_recipient_country_code()
    activity_id = save_activity(identifier, title, description, country, doc_id)
    geocoding = [(data['geocoding'], data['texts']) for (l, data) in results if data.get('geocoding')]
    persist_geocoding(geocoding, doc_id, activity_id)


def persist_geocoding(geocoding_list, doc_id, activity_id):
    for geocoding in geocoding_list:
        geo_id = save_geocoding(geocoding[0], doc_id, activity_id)
        for text in geocoding[1]:
            save_extract_text(text.get('text'), geo_id, ', '.join(text.get('entities')))
    return None


if __name__ == '__main__':
    process_queue()

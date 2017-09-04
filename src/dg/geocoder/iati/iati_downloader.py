# -*- coding: utf-8 -*-
import logging
import os
import uuid
from urllib.parse import unquote_plus
from urllib.request import urlopen

from lxml import etree as et

from dg.geocoder.config import get_download_path
from dg.geocoder.iati.activity_reader import ActivityReader
from dg.geocoder.iati.iati_codes import iati_countries
from dg.geocoder.util.file_util import get_folder_name, create_folder

logger = logging.getLogger()


def download(dest_path, url):
    try:
        file_name = url.split('/')[-1]
        path = os.path.realpath(os.path.join(dest_path, unquote_plus(file_name)))
        if not os.path.exists(path):
            f = urlopen(url)
            headers = f.headers['content-type'].split('/')
            md = 'w'
            if 'html' in headers:
                file_name = '{}.html'.format(uuid.uuid1())
            else:
                md = 'wb'
                with open(path, md) as local_file:
                    local_file.write(f.read())

        if os.path.exists(path):
            return path
        else:
            logger.info("Wasn't able to find the file....!")
            return None
    except Exception as error:
        logger.error('download error %s', error)


def download_activity_data(activity_reader, download_path, dump_activity=False):
    identifier = activity_reader.get_identifier()

    if activity_reader.has_documents():
        downloaded_files = []
        logger.info('Activity %s has documents we will process it ' % identifier)

        region = activity_reader.get_recipient_region_name()
        country = activity_reader.get_recipient_country_name()
        folder_path = 'NA'

        if country is not None:
            folder_path = get_folder_name(country)
        elif region is not None:
            folder_path = get_folder_name(region)

        path = create_folder(
            os.path.join(download_path, get_folder_name(activity_reader.get_reporting_organisation_name()),
                         folder_path))
        path = create_folder(os.path.join(path, identifier))

        if dump_activity:
            # save xml activity in disk
            logger.info('Saving xml file %s' % identifier)
            activity_xml_path = '%s/activity.xml' % path
            f = open(activity_xml_path, 'w')
            f.write(activity_reader.xml())
            f.close()

        logger.info('Getting related documents')

        docs = activity_reader.get_document_links()
        for doc in docs:
            downloaded_files.append(download(path, doc.get('url')))

        return downloaded_files

    else:
        logger.info("Activity %s hasn't any doc type A02 or A07" % identifier)
        return None, None


def bulk_data_download(org, countries=None, download_path=get_download_path(), offset=0, activities_limit=100):
    if countries is None:
        countries = []
    for country in countries:
        logger.info('Searching activities fo %s in country %s' % (org, country))
        url = 'http://datastore.iatistandard.org/api/1/access/activity.xml' \
              '?reporting-org=%s&recipient-country=%s&offset=%s&limit=%s' % (org, country, offset, activities_limit)

        root = et.parse(urlopen(url)).getroot()
        activity_list = root.findall('iati-activities/iati-activity')
        logger.info('Found %d activities ' % (len(activity_list)))
        for activity in activity_list:
            reader = ActivityReader(root=activity)
            download_activity_data(reader, download_path, dump_activity=True)


if __name__ == '__main__':
    bulk_data_download('46002', iati_countries, activities_limit=10)
    bulk_data_download('XI-IATI-IADB', iati_countries, activities_limit=10)

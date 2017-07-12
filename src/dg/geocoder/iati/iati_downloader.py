# -*- coding: utf-8 -*-
import uuid
import xml.etree.ElementTree as ET
from urllib.request import urlopen

from dg.geocoder.iati.activity_reader import ActivityReader
from dg.geocoder.util.file_util import get_folder_name, create_folder


def download(dest_path, url):
    try:
        file_name = url.split('/')[-1]
        f = urlopen(url)
        headers = f.headers['content-type'].split('/')
        md = 'w'
        if 'html' in headers:
            file_name = '%s.html' % uuid.uuid1()
        else:
            md = 'wb'
            path = "%s/%s" % (dest_path, file_name)
            with open(path, md) as local_file:
                local_file.write(f.read())
                print('file saved')
                return path
    except Exception as error:
        print('download error %s', error)


def process_activity(act_doc, download_path='downloads'):
    parser = ActivityReader(root=act_doc)
    identifier = parser.get_identifier()

    if parser.has_documents():
        print('has documents')
        activity_xml = None
        downloaded_files = []

        print('Activity %s has documents we will process it ' % identifier)

        region = parser.get_recipient_region_name()
        country = parser.get_recipient_country_name()
        folder_path = 'NA'

        if country is not None:
            folder_path = get_folder_name(country)
        elif region is not None:
            folder_path = get_folder_name(region)

        path = create_folder('%s/%s/%s' % (download_path, parser.get_reporting_organisation_name(), folder_path))
        path = create_folder(('%s/%s' % (path, identifier)))

        print('Saving xml file %s' % identifier)
        activity_xml = '%s/activity.xml' % path
        f = open(activity_xml, 'w')
        content = ET.tostring(act_doc)
        f.write(content.decode('utf-8'))
        f.close()

        print('Getting related documents')

        docs = parser.get_document_links()
        for doc in docs:
            downloaded_files.append(download(path, doc.get('url')))

        return activity_xml, downloaded_files

    else:
        print("Activity %s hasn't any doc type A02 or A07", identifier)
        return None, None


def bulk_data_download(org, countries=[], download_path='downloads', offset=0, activities_limit=100):
    for country in countries:
        url = 'http://datastore.iatistandard.org/api/1/access/activity.xml' \
              '?reporting-org=%s&recipient-country=%s&offset=%s&limit=%s' % (org, country, offset, activities_limit)

        root = ET.parse(urlopen(url)).getroot()
        activity_list = root.findall('iati-activities/iati-activity')

        for activity in activity_list:
            process_activity(activity, download_path)


def activity_data_download(identifier):
    url = 'http://datastore.iatistandard.org/api/1/access/activity.xml?iati-identifier=%s' % identifier
    root = ET.parse(urlopen(url).read()).getroot()

    activities_files = process_activity(root.findall('iati-activities/iati-activity')[0])
    return activities_files

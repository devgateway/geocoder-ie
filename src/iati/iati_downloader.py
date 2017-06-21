# -*- coding: utf-8 -*-
import xml.etree.ElementTree as ET
import urllib2
import urllib
import os
import errno
import re
import uuid
from iati.activity_reader import ActivityReader
from iati.iati_codes import countries, regions, organisations
from util.file_util import get_folder_name, create_folder

PATH_TO_PROJECTS = '../../corpora/projects'


def download(dest_path, url):
    try:
        file_name = url.split('/')[-1]
        f = urllib2.urlopen(url)
        if 'text' in f.info().maintype:
            md = 'w'
            if 'html' in f.info().getsubtype():
                file_name = '%s.html' % uuid.uuid1()
        else:
            md = 'wb'
            path="%s/%s" % (dest_path, file_name)
            with open(path, md) as local_file:
                local_file.write(f.read())
                print 'file saved'
                return path
    except Exception as inst:
        print(inst.message)


def process_activity(act_doc):
    parser = ActivityReader(root=act_doc)
    if parser.has_documents():
        activity_xml = None
        downloaded_files = []

        identifier = parser.get_identifier()
        print 'Activity %s has documents we will process it ' % identifier

        region = parser.get_recipient_region_name()
        country = parser.get_recipient_country_name()
        folder_path = 'NA'

        if country is not None:
            folder_path = get_folder_name(country)
        elif region is not None:
            folder_path = get_folder_name(region)

        path = create_folder('%s/%s' % (PATH_TO_PROJECTS, parser.get_reporting_organisation_name()), folder_path)
        path = create_folder(path, identifier)

        print 'Saving xml file %s' % identifier
        activity_xml = '%s/activity.xml' % path
        f = open(activity_xml, 'w')
        f.write(ET.tostring(act_doc))
        f.close()

        print 'Getting related documents'

        docs = parser.get_document_links()
        for doc in docs:
            downloaded_files.append(download(path, doc.get('url')))

        return (activity_xml, downloaded_files)

    else:
        print "Activity %s hasn't any doc type A02 or A07"

    return (None, None)

    # return activity_xml adn related files


def bulk_data_download(org, country, offset=0, activities_limit=100):
    url = 'http://datastore.iatistandard.org/api/1/access/activity.xml?reporting-org=%s&recipient-country=%s&offset=0&limit=%s' % \
          (org, country, activities_limit)
    root = ET.parse(urllib.urlopen(url)).getroot()
    activites = root.findall('iati-activities/iati-activity')
    print(len(activites))
    [(process_activity(activity, org)) for activity in activites]


def by_donor_data_download(donor_code):
    for country in countries:
        bulk_data_download(donor_code, country, 0, )


def download_some_data():
    for country in countries:
        if country not in ['GQ', 'GA', 'GM', 'GH', 'GN', 'GW']:
            bulk_data_download('46002', country, offset=0, activities_limit=500)


def activity_data_download(identifier):
    url = 'http://datastore.iatistandard.org/api/1/access/activity.xml?iati-identifier=%s' % identifier
    root = ET.parse(urllib.urlopen(url)).getroot()
    activities_files = process_activity(root.findall('iati-activities/iati-activity')[0])
    return activities_files

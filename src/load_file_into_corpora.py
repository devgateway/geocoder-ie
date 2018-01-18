import logging.config

import argparse
import logging
import sys

import os
from random import shuffle

from dg.geocoder.config import get_log_config_path, get_download_path
from dg.geocoder.data.corpora_generator import generate_docs_list
from dg.geocoder.db.corpora import save_sentences
from dg.geocoder.iati.activity_reader import ActivityReader
from dg.geocoder.iati.iati_downloader import download_activity_data
from dg.geocoder.readers.factory import get_reader
from lxml import etree as et

logging.config.fileConfig(get_log_config_path())
logger = logging.getLogger()


def process_file(file):
    try:
        reader = get_reader(file)
        if reader.is_english_lang():
            logger.info('processing %s' % file.split('/')[-1])
            sentences = reader.split()
            save_sentences(file, sentences)
        else:
            logger.info('ignoring non english file')

    except Exception as error:
        logger.info(error)


def process_xml(file):
    download_path = '/tmp'

    root = et.parse(file).getroot()
    activity_list = root.findall('iati-activities/iati-activity')

    logger.info('Found %d activities ' % (len(activity_list)))
    for activity in activity_list:
        reader = ActivityReader(root=activity)
        download_activity_data(reader, download_path=download_path , dump_activity=True)

    docs_to_process = []
    generate_docs_list(os.path.abspath(download_path ), docs_to_process)
    shuffle(docs_to_process)
    logger.info('There are %s documents, we will take a random subset of 200 ' % len(docs_to_process))
    for path, file in docs_to_process:
        process_file(path, file)


def main(args):
    parser = argparse.ArgumentParser(description="Auto-geocode activity projects")
    parser.add_argument("-f", "--file")
    parser.add_argument("-x", "--xml")
    args = parser.parse_args(args)

    if args.file:
        process_file(args.file)

    if args.xml:
        process_xml(args.xml)


# report error and proceed
if __name__ == '__main__':
    main(sys.argv[1:])

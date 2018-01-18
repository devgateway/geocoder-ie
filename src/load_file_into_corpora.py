import logging.config

import argparse
import logging
import sys

import os

from dg.geocoder.config import get_log_config_path
from dg.geocoder.db.corpora import save_sentences
from dg.geocoder.readers.factory import get_reader

logging.config.fileConfig(get_log_config_path())
logger = logging.getLogger()


def process_file(file):
    try:
        reader = get_reader(file)
        if reader.is_english_lang():
            logger.info('processing %s' % file.split('/')[-1])
            sentences = reader.split()
            save_sentences(file, sentences )
        else:
            logger.info('ignoring non english file')

    except Exception as error:
        logger.info(error)


def main(args):
    parser = argparse.ArgumentParser(description="Auto-geocode activity projects")
    parser.add_argument("-f", "--file")
    args = parser.parse_args(args)
    if args.file:
        process_file(args.file)


# report error and proceed
if __name__ == '__main__':
    main(sys.argv[1:])

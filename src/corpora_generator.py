import logging
import os
import random
from os import walk
from random import shuffle

from dg.geocoder.db.corpora import clean, save_sentences
from dg.geocoder.readers.factory import get_reader

logger = logging.getLogger()

download_path = 'download'


def is_valid_type(file):
    ex = file.split('.')[-1]
    return ex.lower() in ['pdf', 'odt']


def process_file(dir_path, file):
    web_path = '/'.join(dir_path.split(os.path.sep)[dir_path.split(os.path.sep).index('download'):])

    try:
        reader = get_reader(os.path.join(dir_path, file))
        if reader.is_english_lan():
            logger.info('processing %s' % file)
            save_sentences('%s/%s' % (web_path, file), reader.split())
        else:
            logger.info('ignoring non english file')

    except Exception as error:
        logger.info(error)


def generate_docs_list(folder, doc_list):
    for (dir_path, dir_names, file_names) in walk(folder):
        for f in file_names:
            if is_valid_type(f):
                doc_list.append((dir_path, f))
        for folder in dir_names:
            generate_docs_list(folder, doc_list)


def generate():
    clean()
    docs_to_process = []
    generate_docs_list(os.path.abspath(download_path), docs_to_process)
    shuffle(docs_to_process)
    logger.info('There are %s documents, we will take a random subset of 200 ' % len(docs_to_process))
    sample = random.sample(docs_to_process, 200)
    for path, file in sample:
        process_file(path, file)


if __name__ == '__main__':
    generate()

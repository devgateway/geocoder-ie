import os
import random
from os import walk

from langdetect import detect

from dg.geocoder.db.corpora import save_sentences, clean
from dg.geocoder.readers.odt_reader import OdtReader
from dg.geocoder.readers.pdf_reader import PdfReader

download_path = 'download'

def is_valid_type(file):
    ex = file.split('.')[-1]
    return ex.lower() in ['pdf', 'odt']


def process_file(dir_path, file):
    web_path='/'.join(dir_path.split(os.path.sep)[dir_path.split(os.path.sep).index('download'):])

    try:
        f_ex = file.split('.')[-1]
        if f_ex.lower() == 'pdf':
            print('pdf file ')
            pdf = PdfReader(os.path.join(dir_path, file))
            if detect(pdf.get_page(1)) == 'en':
                save_sentences('%s/%s' % (web_path,file), pdf.split())

        elif f_ex.lower() == 'odt':
            odt = OdtReader(os.path.join(dir_path, file))
            if detect(odt.split()[1]) == 'en':
                save_sentences('%s/%s' % (web_path,file), odt.split())

    except Exception as error:
        print(error)


def generate_docs_list(folder, list):
    for (dir_path, dir_names, file_names) in walk(folder):
        for f in file_names:
            if is_valid_type(f):
                list.append((dir_path, f))
        for folder in dir_names:
            generate_docs_list(folder, list)


if __name__ == '__main__':
    clean()
    docs_to_process = []
    generate_docs_list(os.path.abspath(download_path), docs_to_process)
    sample = random.sample(docs_to_process, 100)
    for path, file in sample:
        process_file(path, file)

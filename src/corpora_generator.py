import os
from importlib._bootstrap_external import _path_join

from os import walk
from sys import path

from langdetect import detect

from dg.geocoder.readers.odt_reader import OdtReader
from dg.geocoder.readers.pdf_reader import PdfReader


def save_sentences(reader):
    print(reader)


def process_file(dirpath, file):
    try:
        f_ex = file.split('.')[-1]
        if f_ex.lower() == 'pdf_':
            print('pdf file ')
            pdf = PdfReader(_path_join(dirpath, file))
            if detect(pdf.get_page(1)):
                save_sentences(pdf.split())

        elif f_ex.lower() == 'odt':
            odt = OdtReader(_path_join(dirpath, file))
            if detect(odt.split()[1]) == 'en':
                save_sentences(odt.split())

    except Exception as error:
        print(error)


def generate_database_corpora(files_path='download'):
    for (dir_path, dir_names, file_names) in walk(files_path):
        for f in file_names:
            process_file(dir_path, f)
        for folder in dir_names:
            generate_database_corpora(folder)


if __name__ == '__main__':
    print(detect("War doesn't show who's right, just who's left."))
    generate_database_corpora(path=os.path.abspath('download'))

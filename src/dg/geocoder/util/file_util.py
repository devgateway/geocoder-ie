import errno
import os
import re

PDF = 'pdf'
ODT = 'odt'
HTML = 'html'
XML = 'xml'


def is_pdf(name):
    return get_file_type(name) == PDF


def is_odt(name):
    return get_file_type(name) == ODT


def is_html(name):
    return get_file_type(name) == HTML


def is_xml(name):
    return get_file_type(name) == XML


# todo use libmagic
def get_file_type(name):
    f_ex = name.split('.')[-1]
    return f_ex.lower()


def get_folder_name(name):
    return re.sub(re.compile('[^0-9a-zA-Z]+'), '_', name).lower()


def create_folder(path):
    if not os.path.exists(os.path.realpath(path)):
        try:
            os.makedirs(os.path.realpath(path))

        except OSError as exc:  # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise
    return path

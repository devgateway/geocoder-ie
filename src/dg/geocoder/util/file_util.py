import errno
import os
import re

PDF = 'pdf'
ODT = 'odt'
HTML = 'html'
XML = 'xml'
TXT = 'txt'

valid_formats = [PDF, HTML, XML, TXT, ODT]


def is_valid(name):
    return get_file_type(name) in valid_formats


def is_pdf(name):
    return get_file_type(name) == PDF


def is_odt(name):
    return get_file_type(name) == ODT


def is_html(name):
    return get_file_type(name) == HTML


def is_xml(name):
    return get_file_type(name) == XML


def is_txt(name):
    return get_file_type(name) == TXT


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

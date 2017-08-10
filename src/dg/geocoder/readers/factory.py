from dg.geocoder.readers.odt_reader import OdtReader
from dg.geocoder.readers.pdf_reader import PdfReader
from dg.geocoder.readers.text_reader import TextReader
from dg.geocoder.util.file_util import is_pdf, is_odt


def get_reader(path_to_file):
    if is_pdf(path_to_file):
        print('Creating pdf reader for file {}'.format(path_to_file))
        return PdfReader(path_to_file)
    elif is_odt(path_to_file):
        print('Creating odt reader')
        return OdtReader(path_to_file)
    else:
        return None


def get_text_reader(text):
    return TextReader(text)

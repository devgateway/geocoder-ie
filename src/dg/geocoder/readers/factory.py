from dg.geocoder.readers.odt_reader import OdtReader
from dg.geocoder.readers.pdf_reader import PdfReader
from dg.geocoder.util.file_util import is_pdf, is_odt


def get_reader(path_to_file):
    if is_pdf(path_to_file):
        return PdfReader(path_to_file)
    elif is_odt(path_to_file):
        return OdtReader(path_to_file)

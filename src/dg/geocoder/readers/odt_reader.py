import zipfile
import xml.etree.ElementTree as ET
import nltk

from dg.geocoder.readers.base_reader import BaseReader, get_sentence_tokenizer


class OdtReader(BaseReader):
    def __init__(self, file):
        self.file = file
        self.paragraphs = []
        zip_archive = zipfile.ZipFile(file, "r")
        self.doc = ET.parse(zip_archive.open("content.xml"))
        self.text = ''
        for part in self.doc.getroot().itertext():
            self.text = self.text + '\n' + part

    def split(self):
        if len(self.paragraphs) == 0:
            self.paragraphs = [(e.replace('\n', ' ')) for e in get_sentence_tokenizer().tokenize(self.text)]
        return self.paragraphs

    def get_sample(self):
        return self.split()[1]
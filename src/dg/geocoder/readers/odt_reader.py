import zipfile
import xml.etree.ElementTree as ET
import nltk


class OdtReader:
    def __init__(self, file):
        self.sentence_tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
        self.file = file
        self.paragraphs = []
        zip_archive = zipfile.ZipFile(file, "r")
        self.doc = ET.parse(zip_archive.open("content.xml"))
        self.text = ''
        for part in self.doc.getroot().itertext():
            self.text = self.text + '\n' + part

    def split(self):
        if len(self.paragraphs) == 0:
            self.paragraphs = [(e.replace('\n', ' ')) for e in self.sentence_tokenizer.tokenize(self.text)]
        return self.paragraphs

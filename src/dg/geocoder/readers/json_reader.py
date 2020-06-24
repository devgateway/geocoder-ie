import re

from bs4 import BeautifulSoup
from dg.geocoder.readers.base_reader import BaseReader

TAG_RE = re.compile(r'<[^>]+>')


def remove_tags(text):
    soup = BeautifulSoup(text, 'html.parser')
    return soup.getText().strip()


class JsonReader(BaseReader):
    def __init__(self, j_object):
        super().__init__()
        self.file = None
        self.jo = j_object
        self.texts = []
        self.paragraphs = []

    def split(self):
        for p in self.jo:
            a_text = self.jo[p]
            if a_text is not None and isinstance(a_text, str):
                a_text = remove_tags(a_text)
                paragraphs = [e for e in self.get_sentence_tokenizer().tokenize(a_text)]
                for p_text in paragraphs:
                    self.paragraphs.append([p, p_text])

        return self.paragraphs

    def get_sample(self):
        list = [a for a in [self.jo[c] for c in self.jo] if isinstance(a, str) and len(a) > 50]
        if len(list) > 0:
            return list[0]

        return ''

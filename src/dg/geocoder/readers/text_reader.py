from dg.geocoder.readers.base_reader import BaseReader, get_sentence_tokenizer


class TextReader(BaseReader):
    def __init__(self, text):
        self.text = text
        self.paragraphs = []

    def split(self):
        if len(self.paragraphs) == 0:
            self.paragraphs = [(e.replace('\n', ' ')) for e in get_sentence_tokenizer().tokenize(self.text)]
        return self.paragraphs

    def get_sample(self):
        return self.split()[0]

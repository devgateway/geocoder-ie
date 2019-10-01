from dg.geocoder.readers.base_reader import BaseReader


class TextReader(BaseReader):
    def __init__(self, text):
        super().__init__()
        self.file = None
        self.text = text
        self.paragraphs = []

    def split(self):
        if len(self.paragraphs) == 0:
            self.paragraphs = [(e, self.file) for e in self.get_sentence_tokenizer().tokenize(self.text)]
        return self.paragraphs

    def get_sample(self):
        return self.split()[0]

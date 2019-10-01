from dg.geocoder.readers.base_reader import BaseReader


class TxtReader(BaseReader):
    def __init__(self, file):
        super().__init__()
        self.file = file
        self.paragraphs = []

    def split(self):
        if len(self.paragraphs) == 0:
            with open(self.file, "rt") as f:
                text = f.read()
            self.paragraphs = [(self.file, e) for e in self.get_sentence_tokenizer().tokenize(text)]
            f.close()

        return self.paragraphs

    def get_sample(self):
        return self.split()[0]

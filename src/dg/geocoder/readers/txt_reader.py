from dg.geocoder.readers.base_reader import BaseReader, get_sentence_tokenizer


class TxtReader(BaseReader):
    def __init__(self, file):
        self.file = file
        self.paragraphs = []

    def split(self, n=None):
        if len(self.paragraphs) == 0:
            with open(self.file, "rt", encoding="utf-8") as f:
                text = f.read()
            self.paragraphs = [e for e in get_sentence_tokenizer().tokenize(text)]
            f.close()

        return self.paragraphs

    def get_sample(self):
        return self.split()[0]

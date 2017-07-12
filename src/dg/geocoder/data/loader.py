import os
import numpy
from pandas import DataFrame
from sner import Ner
tagger = Ner(host='localhost', port=1234)

class FileDataLoader:
    def __init__(self, path=''):
        self.path = path
        self.confusion = numpy.array([[0, 0], [0, 0]])

    def read_files(self, encoding="utf-8"):
        for root, dir_names, file_names in os.walk(self.path):
            for path in dir_names:
                self.read_files(os.path.join(root, path))
            for file_name in file_names:
                file_path = os.path.join(root, file_name)
                if os.path.isfile(file_path):
                    f = open(file_path, encoding=encoding)
                    content = f.read()
                    classification = file_path.split(os.path.sep)[-2]
                    yield file_path, content, classification

    def build_data_frame(self, remove_entities=False):
        rows = []
        index = []
        for file_name, text, classification in self.read_files():
            index.append(file_name)
            if remove_entities:
                tagged = tagger.get_entities(text)
                entities = [a for a, b in tagged if b in ['LOCATION']]
                stripped_text = ' '.join([(t) for t in text.split(' ') if t not in entities])
                rows.append({'text': stripped_text, 'class': classification})
            else:
                rows.append({'text': text, 'class': classification})

        data_frame = DataFrame(rows, index=index)
        data_frame = data_frame.reindex(numpy.random.permutation(data_frame.index))

        return data_frame

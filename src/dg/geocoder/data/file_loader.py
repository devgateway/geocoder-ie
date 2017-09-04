import os

import numpy
from pandas.core.frame import DataFrame


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

    def build_data_frame(self):
        rows = []
        index = []
        for file_name, text, classification in self.read_files():
            index.append(file_name)
            rows.append({'text': text, 'class': classification})

        data_frame = DataFrame(rows, index=index)
        data_frame = data_frame.reindex(numpy.random.permutation(data_frame.index))

        return data_frame

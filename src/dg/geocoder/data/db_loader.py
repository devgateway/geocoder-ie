import numpy
from numpy import random
from pandas.core.frame import DataFrame
from sner.client import Ner

from dg.geocoder.db.corpora import get_sentences


class DbDataLoader:

    def get_geography_rows(self, limit=2000):
        return get_sentences(category='geography', limit=limit)['rows']

    def get_none_rows(self, limit=2000):
        return get_sentences(category='none', limit=limit)['rows']

    def read_rows(self):
        geography_records = self.get_geography_rows()
        # get same amount of none records
        none_records = self.get_none_rows(limit=len(geography_records))
        all_records = geography_records + none_records
        random.shuffle(all_records)
        return all_records

    def build_data_frame(self, remove_entities=False):

        rows = []
        index = []
        for id, text, classification, file_name in self.read_rows():
            index.append(id)
            rows.append({'text': text, 'class': classification})

        data_frame = DataFrame(rows, index=index)
        data_frame = data_frame.reindex(numpy.random.permutation(data_frame.index))

        return data_frame

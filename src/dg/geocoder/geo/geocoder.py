import time
from os.path import isfile

import numpy as np
import pycorenlp.corenlp

from dg.geocoder.classification.classifier import load_classifier
from dg.geocoder.config import get_ner_host, get_ner_port, get_ignore_entities, get_ignore_gap_chars
from dg.geocoder.geo.geonames import resolve
from dg.geocoder.readers.factory import get_text_reader, get_reader


def process_activity(activity):
    print(activity)


def bulk_process(xml, path_to_docs='docs'):
    if xml is None:
        print('xml file should be provide')
    else:
        print('Process list of activities')


def classify(text=None, file=None, cls_name='default_classifier'):
    if file is not None:
        if not isfile(file):
            raise SystemError("Can't find {}".format(file))
        reader = get_reader(file)
    else:
        reader = get_text_reader(text)

    if reader is None:
        raise SystemError("Wasn't able to initialize a reader check file type and extension ".format(file))
    tic = time.clock()
    # split document in sentences
    sentences = reader.split()
    toc = time.clock()

    print('There are {count} sentences to process, split took {time}ms '.format(count=len(sentences), time=toc - tic))
    classifier = load_classifier(cls_name)
    predicted = classifier.predict(sentences)
    indexes = np.where(predicted == 'geography')[0]
    print('{} geographical sentences found '.format(len(indexes)))

    geo_sentences = [(sentences[i]) for i in indexes]
    return geo_sentences


# merge equals names and join texts
def join(list):
    locs = {}
    for item in list:
        for l in item['locations']:
            if locs.get(l):
                locs[l]['texts'].append({'text': item['text'], 'entities': item['entities']})
            else:
                locs[l] = {'texts': [{'text': item['text'], 'entities': item['entities']}]}

    return [(key, locs[key]) for key in locs]


# query geonames an get geographical information
def geonames(list, country_codes=[]):
    for name, metadata in list:
        coding = resolve(name, country_codes=country_codes)
        if coding is not None:
            metadata['geocoding'] = coding

    return list


# Perform natural language processing to text, get annotated entities and entities relations
def extract(sentences, ignore_entities=get_ignore_entities()):
    tic = time.clock()
    nlp = pycorenlp.corenlp.StanfordCoreNLP("http://{0}:{1}/".format(get_ner_host(), get_ner_port()))
    extraction = []

    for s in sentences:
        output = nlp.annotate(s.replace('\n', ' '), properties={"annotators": "openie,ner", "outputFormat": "json"})
        relations = [output["sentences"][0]["openie"] for item in output]
        locations_found = [(t['originalText']) for t in output["sentences"][0]["tokens"] for item in output if
                           t['ner'] in ['LOCATION', 'PERSON'] and t['originalText'].lower() not in ignore_entities]
        if len(locations_found) > 0:
            extraction.append(({'text': s, 'entities': locations_found, 'relations': relations}))

    tac = time.clock()
    print('NER extraction took {time}ms'.format(time=tac - tic))
    return extraction


def gap_length(word1, word2, text):
    start_1 = text.index(word1)
    start_2 = text.index(word2)

    end_1 = start_1 + len(word1)
    # end_2 = start_2 + len(word2)
    gap = start_2 - end_1
    connection_text = text[end_1:start_2]
    edited_text = chr(0) * end_1 + text[end_1:]
    return gap, connection_text, edited_text


def merge(extracted, distance=2, ignored_gap_chars=get_ignore_gap_chars()):
    ret_val = []
    for row in extracted:
        text = row['text']
        entities = row['entities']
        x = 0
        last_idx = len(entities) - 1
        merged = []

        # ierate locations
        while x <= last_idx:
            to_merge = entities[x]

            while x is not last_idx:
                current_loc = entities[x]
                next_loc = entities[x + 1]
                # get the gap bewteen the two entities
                gap, connection_text, text = gap_length(current_loc, next_loc, text)
                # if gap is < to distance but there are special chars in between we take them as separate
                # entities ie Congo,Burkina will be taken as ['Congo','Burkina'] and Congo,New Guinea,
                # Burkina will be taken as ['Congo','New Guinea','Burkina']
                if gap < distance and connection_text not in ignored_gap_chars:
                    to_merge += ' ' + next_loc
                    x += 1
                else:
                    break
            x += 1
            merged.append(to_merge)
        row['locations'] = merged
    return extracted


def geocode(text=None, file=None, cls_name='default_classifier', country_codes=[]):
    texts = ''
    results = None
    # 1) classify paragraph and filter out what doesn't refer to project geographical information
    # 2) extract entities and relationships
    # 3) merge names
    # 3) resolve locations using Geo Names
    return geonames(join(merge(extract(classify(text=text, file=file, cls_name=cls_name)
                                       )
                               )), country_codes=country_codes)

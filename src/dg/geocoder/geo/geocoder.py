import time
from os.path import isfile

import numpy as np
import pycorenlp.corenlp

from dg.geocoder.classification.classifier import load_classifier
from dg.geocoder.config import get_ner_host, get_ner_port, get_ignore_entities, get_ignore_gap_chars, \
    get_default_classifier
from dg.geocoder.geo.geonames import resolve
from dg.geocoder.readers.factory import get_reader, get_text_reader


def process_activity(activity):
    print(activity)


def bulk_process(xml, path_to_docs='docs'):
    if xml is None:
        print('xml file should be provide')
    else:
        print('Process list of activities')


def classify(texts, files, cls_name):
    # extract sentences from files
    tic = time.clock()
    sentences = []
    for text in texts:
        reader = get_text_reader(text)
        if reader.is_english_lan():
            sentences += reader.split()
            reader = None
        else:
            print('Non english text, it will be ignored')

    for file in files:

        if file is not None:
            if not isfile(file):
                raise SystemError("Can't find {}".format(file))
            reader = get_reader(file)
            if reader is None:
                print("Wasn't able to initialize a reader check file type and extension fro {}".format(file))
            # split document in sentences
            elif not reader.is_english_lan():
                print('Non english document it will be ignored')
            else:
                sentences += reader.split()
                reader = None

    toc = time.clock()
    print('There are {count} sentences to process, split took {time}ms '.format(count=len(sentences), time=toc - tic))
    classifier = load_classifier(cls_name)
    predicted = classifier.predict(sentences)
    indexes = np.where(predicted == 'geography')[0]
    print('{} geographical sentences found '.format(len(indexes)))
    geo_sentences = [(sentences[i]) for i in indexes]
    sentences = None

    return geo_sentences


# merge equals names and join texts
def join(list):
    locs = {}
    for item in list:
        for l in item['locations']:
            if locs.get(l.lower()):
                locs[l.lower()]['texts'].append({'text': item['text'], 'entities': item['entities']})
            else:
                locs[l.lower()] = {'texts': [{'text': item['text'], 'entities': item['entities']}]}

    return [(key, locs[key]) for key in locs]


# query geonames an get geographical information
def geonames(list, cty_codes=[]):
    for name, metadata in list:
        coding = resolve(name, cty_codes)
        if coding is not None:
            metadata['geocoding'] = coding

    return list


# Perform natural language processing to text, get annotated entities and entities relations
def extract(sentences, ignore_entities=get_ignore_entities()):
    tic = time.clock()
    nlp = pycorenlp.corenlp.StanfordCoreNLP("http://{0}:{1}/".format(get_ner_host(), get_ner_port()))
    extraction = []

    for s in sentences:
        output = nlp.annotate(s, properties={"annotators": "openie,ner", "outputFormat": "json"})
        relations = [output["sentences"][0]["openie"] for item in output]
        locations_found = [(t['originalText']) for t in output["sentences"][0]["tokens"] for item in output if
                           t['ner'] in ['LOCATION', 'PERSON'] and t[
                               'originalText'].lower() not in ignore_entities]
        if len(locations_found) > 0:
            extraction.append(({'text': s, 'entities': locations_found, 'relations': relations}))

    tac = time.clock()
    print('NER extraction took {time}ms'.format(time=tac - tic))
    return extraction


def gap_length(word1, word2, text):
    start_1 = text.index(word1)
    start_2 = text.index(word2, start_1 + len(word1))
    end_1 = start_1 + len(word1)
    # end_2 = start_2 + len(word2)
    gap = start_2 - end_1
    connection_text = text[end_1:start_2]
    edited_text = chr(0) * end_1 + text[end_1:]
    return gap, connection_text, edited_text


def merge(extracted, distance=2, ignored_gap_chars=get_ignore_gap_chars()):
    ret_val = []
    for row in extracted:
        text = ' '.join(row['text'].replace('\n\n', ', ').split())
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


def geocode(texts, documents, cty_codes, cls_name=get_default_classifier(), persits=False):
    # 1) classify paragraph and filter out what doesn't refer to project geographical information
    # 2) extract entities and relationships
    # 3) merge names
    # 3) resolve locations using Geo Names
    texts = classify(texts, documents, cls_name=cls_name)
    entities = merge(extract(texts))
    normalized = join(entities)
    if persits:
        pass
        # save to database
    return geonames(normalized, cty_codes=cty_codes)

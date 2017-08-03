import numpy as np
import pycorenlp.corenlp

from dg.geocoder.classification.classifier import load_classifier
from dg.geocoder.config import get_ner_host, get_ner_port
from dg.geocoder.geo.geonames import query, search
from dg.geocoder.readers.factory import get_text_reader, get_reader


def process_activity(activity):
    print(activity)


def bulk_process(xml, path_to_docs='docs'):
    if xml is None:
        print('xml file should be provide')
    else:
        print('Process list of activities')


def classify(text=None, file=None, cls_name='default_classifier'):
    reader = None
    if file is not None:
        reader = get_reader(file)
    else:
        reader = get_text_reader(text)

    # split document in sentences
    sentences = reader.split()
    classifier = load_classifier(cls_name)
    predicted = classifier.predict(sentences)
    indexes = np.where(predicted == 'geography')[0]
    geo_sentences = [(sentences[i]) for i in indexes]
    return geo_sentences


# query geonames an get geographical information
def geonames(list, country_codes=[]):
    for i in range(len(list)):
        row = list[i]
        locations = row['locations']
        relations = row['relations'][i]
        rels = [(r.get('object')) for r in relations if r['relation'] == 'is in']
        for l in locations:
            results = search(l, country_codes=country_codes, rels=rels)
    return None


# Perform natural language processing to text, get annotated entities and entities relations
def extract(sentences):
    nlp = pycorenlp.corenlp.StanfordCoreNLP("http://{0}:{1}/".format(get_ner_host(), get_ner_port()))
    extraction = []

    for s in sentences:
        output = nlp.annotate(s.replace('\n', ' '), properties={"annotators": "openie,ner", "outputFormat": "json"})
        relations = [output["sentences"][0]["openie"] for item in output]
        locations_found = [(t['originalText']) for t in output["sentences"][0]["tokens"] for item in output if
                           t['ner'] == 'LOCATION']
        if len(locations_found) > 0:
            extraction.append(({'text': s, 'entities': locations_found, 'relations': relations}))

    return extraction


def gap_length(word1, word2, text):
    start_1 = text.index(word1)
    start_2 = text.index(word2)

    end_1 = start_1 + len(word1)
    end_2 = start_2 + len(word2)
    gap = start_2 - end_1
    connection_text = text[end_1:start_2]
    edited_text = chr(0) * end_1 + text[end_1:]
    return gap, connection_text, edited_text


def merge(extracted, distance=2, ignored_gap_chars=[',', '-']):
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

    return geonames(merge(extract(classify(text=text, file=file, cls_name=cls_name))), country_codes=country_codes)

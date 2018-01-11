import logging
import time
from os.path import isfile

import numpy as np
import pycorenlp.corenlp
from sner.client import Ner

from dg.geocoder.classification.classifier import load_classifier
from dg.geocoder.config import get_ner_host, get_ner_port, get_ignore_entities, get_ignore_gap_chars, \
    get_default_classifier, get_standford_server_type
from dg.geocoder.geo.geonames import resolve
from dg.geocoder.readers.factory import get_reader, get_text_reader

logger = logging.getLogger()


def classify(texts, files, cls_name):
    # extract sentences from files
    tic = time.clock()
    sentences = []
    geo_sentences = []
    doc_names = []

    for text in texts:
        reader = get_text_reader(text)
        eng = reader.is_english_lang()
        if eng:
            sentences += reader.split()
        else:
            logger.warning('Non english text, it will be ignored')

    doc_names[len(doc_names):] = ["activity.xml"] * len(sentences)

    for file in files:
        if file is not None:
            if not isfile(file):
                raise SystemError("Can't find {}".format(file))
            reader = get_reader(file)
            if reader is None:
                logger.warning("Wasn't able to initialize a reader check file type and extension fro {}".format(file))
            # split document in sentences
            elif not reader.is_english_lang():
                logger.info('Non english document it will be ignored')
            else:
                sentences += reader.split()
                doc_names[len(doc_names):] = [file] * (len(sentences) - len(doc_names))

            reader = None

    toc = time.clock()
    logger.info(
        'There are {count} sentences to process, split took {time}ms '.format(count=len(sentences), time=toc - tic))

    if len(sentences) > 0:
        classifier = load_classifier(cls_name)
        predicted = classifier.predict(sentences)
        indexes = np.where(predicted == 'geography')[0]
        logger.info('{} geographical sentences found '.format(len(indexes)))
        geo_sentences = [(sentences[i], doc_names[i]) for i in indexes]

    return geo_sentences


# merge equals names and join texts
def join(item_list):
    locs = {}
    for item in item_list:
        for l in item['locations']:
            current = l.lower().strip()
            if locs.get(current):
                locs[current]['texts'].append({'text': item['text'], 'entities': item['entities']})
            else:
                locs[current] = {'texts': [{'text': item['text'], 'entities': item['entities']}]}

    return [(key, locs[key]) for key in locs]


# query geonames an get geographical information
def geonames(entity_list, cty_codes=None):
    if cty_codes is None:
        cty_codes = []
    for name, metadata in entity_list:
        coding = resolve(name, cty_codes)
        if coding is not None:
            metadata['geocoding'] = coding

    return entity_list


# Perform natural language processing to text, get annotated entities and entities relations
def extract(sentences, ignore_entities=get_ignore_entities()):
    tic = time.clock()
    nlp = pycorenlp.corenlp.StanfordCoreNLP("http://{0}:{1}/".format(get_ner_host(), get_ner_port()))
    extraction = []

    for s in sentences:
        output = nlp.annotate(s, properties={"annotators": "ner", "outputFormat": "json"})
        locations_found = [(t['originalText']) for t in output["sentences"][0]["tokens"] for item in output if
                           t['ner'] in ['LOCATION', 'PERSON'] and t[
                               'originalText'].lower() not in ignore_entities]
        if len(locations_found) > 0:
            extraction.append(({'text': s, 'entities': locations_found}))

    tac = time.clock()
    logger.info('NER extraction took {time}ms'.format(time=tac - tic))
    return extraction


# Perform natural language processing to text, get annotated entities and entities relations
def extract_ner(sentences, ignore_entities=get_ignore_entities()):
    try:
        tagger = Ner(host=get_ner_host(), port=get_ner_port())
        tic = time.clock()
        extraction = []

        for s, file in sentences:
            output = tagger.get_entities(s.replace('\n', ' ').replace('\r', ''))
            locations_found = [text for text, tag in output if
                               tag in ['LOCATION', 'PERSON'] and text.lower() not in ignore_entities]

            if len(locations_found) > 0:
                extraction.append(({'text': {'text': s, 'file': file}, 'entities': locations_found}))

        tac = time.clock()
        logger.info('NER extraction took {time}ms'.format(time=tac - tic))
        return extraction
    except Exception as detail:
        logger.error('Error during ner extraction {}'.format(detail))
        raise


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
    for row in extracted:
        text = ' '.join(row['text']['text'].replace('\n\n', ', ').split())
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
                # get the gap between  two entities
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


def reduce(results):
    unique_results = {}
    for name, metadata in results:
        geocoding = metadata.get('geocoding')
        if geocoding is not None:
            geonameId = geocoding.get('geonameId')
            existing = unique_results.get(geonameId)
            if existing:
                existing[1]['texts'] = existing[1]['texts'] + metadata['texts']
            else:
                unique_results[geonameId] = (name, metadata)
        else:
            unique_results[name] = (name, metadata)

    return list(unique_results.values())


def geocode(texts, documents, cty_codes, cls_name=get_default_classifier(), step_log=None):
    # 1) classify paragraph and filter out what doesn't refer to project geographical information
    # 2) extract entities and relationships
    # 3) merge names
    # 4) resolve locations using Geo Names
    if step_log:
        step_log("Step 1/4: Classifying documents")

    # texts = classify(texts, set(documents), cls_name=cls_name)

    texts = classify(texts, set(documents), cls_name=cls_name)

    if step_log:
        step_log("Step 2/3: Extracting entities")

    if get_standford_server_type() == 'CORE':
        entities = merge(extract(texts))
    elif get_standford_server_type() == 'NER':
        entities = merge(extract_ner(texts))
    else:
        raise ValueError('Wrong standford server type')

    if step_log:
        step_log("Step 3/4: Normalizing entities")

    normalized = join(entities)

    if step_log:
        step_log("Step 4/4 Geocoding entities")

    results = geonames(normalized, cty_codes=cty_codes)
    reduced = reduce(results)

    return reduced

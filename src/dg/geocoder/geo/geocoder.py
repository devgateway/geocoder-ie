import numpy as np
import pycorenlp.corenlp
from sner import Ner

from dg.geocoder.classification.classifier import load_classifier
from dg.geocoder.config import get_ner_host, get_ner_port
from dg.geocoder.geo.result_parser import CodingResults
from dg.geocoder.readers.factory import get_reader, get_text_reader


def process_activity(activity):
    print(activity)


def bulk_process(xml, path_to_docs='docs'):
    if xml is None:
        print('xml file should be provide')
    else:
        print('Process list of activities')


def classify(sentences, cls_name='default_classifi2er'):
    classifier = load_classifier(cls_name)
    predicted = classifier.predict(sentences)
    return np.where(predicted == 'geography')[0]


def classify_document(file, **kwargs):
    reader = get_reader(file)
    # split document in stences
    sentences = reader.split()
    indexes = classify(sentences, **kwargs)
    geo_sentences = [(sentences[i]) for i in indexes]
    return geo_sentences


def classify_text(text, **kwargs):
    reader = get_text_reader(text)
    # split document in stences
    sentences = reader.split()
    indexes = classify(sentences, **kwargs)
    geo_sentences = [(sentences[i]) for i in indexes]
    return geo_sentences


def get_relations(output, location):
    result = [output["sentences"][0]["openie"] for item in output]
    rels = []
    for i in result:
        for rel in i:
            if rel['subject'] == location or rel['object'] == location:
                rels.append((rel['subject'], rel['relation'], rel['object']))

    return rels


def nlp(sentences):
    nlp = pycorenlp.corenlp.StanfordCoreNLP("http://{0}:{1}/".format(get_ner_host(), get_ner_port()))
    tagged_sentences = []

    for s in sentences:
        output = nlp.annotate(s.replace('\n', ' '), properties={"annotators": "openie,ner", "outputFormat": "json"})
        locations_found = [(t['originalText'], get_relations(output, t['originalText'])) for t in
                           output["sentences"][0]["tokens"]
                           for item in output if
                           t['ner'] == 'LOCATION']

        if len(locations_found) > 0:
            tagged_sentences.append((s, locations_found))

    return tagged_sentences


def tag_sentences(sentences):
    tagger = Ner(host=get_ner_host(), port=get_ner_port())
    tagged_sentences = []
    for s in sentences:
        tagged = tagger.get_entities(s.replace('\n', ' '))
        locs = [(word.strip()) for word, tag in tagged if tag in ['LOCATION']]
        if len(locs) > 0:
            tagged_sentences.append((s, locs))
    return tagged_sentences


def geocode(text=None, file=None, cls_name='default_classifier'):
    texts = ''
    results = None

    if text is not None:
        texts = classify_text(text, cls_name=cls_name)
        results = CodingResults(nlp(texts)).get_results()

    elif file is not None:
        texts = classify_document(file, cls_name=cls_name)
        results = CodingResults(nlp(texts)).get_results()
    else:
        raise ValueError('you must provide a file or a text input ')

    return results

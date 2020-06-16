import inspect
import logging
import time

import rpyc
from rpyc.utils.server import ThreadedServer

import spacy

npl = None
nlp = spacy.load('fr_core_news_md', disable=['tagger', 'parser', 'textcat'])

logger = logging.getLogger()


def extract_spacy(sentences):
    tic = time.clock()
    pos = 0
    extraction = []
    for doc in nlp.pipe([a for a, b in sentences], disable=["tagger"]):
        # Do something with the doc here
        locations = [ent.text for ent in doc.ents if ent.label_ in 'LOC']

        if len(locations) > 0:
            # items = [(l, {'field': sentences[pos][1], 'text': doc.text, 'entities': locations}) for l in locations]
            extraction.append({'text': {'text': doc.text, 'field': sentences[pos][1]}, 'entities': locations})
        pos = pos + 1

    tac = time.clock()
    logger.info('NER extraction took {time}ms'.format(time=tac - tic))
    return extraction


class EchoService(rpyc.Service):
    def on_connect(self, conn):
        pass

    def on_disconnect(self, conn):
        pass

    def exposed_ner(self, sentences):
        return extract_spacy(sentences)


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    server = ThreadedServer(EchoService, port=18861)
    server.start()

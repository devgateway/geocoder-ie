# -*- coding: utf-8 -*-

import nltk
from sner import Ner
from pdf.pdf_reader import Pdfreader
from classifier import get_trained_classifier, bag_of_words, get_tokenizer

tagger = Ner(host='localhost', port=1234)

print ('Loading tokenizers/punkt/english.pickle')
sentence_tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
print ('Sentence Tokenizer ready')

word_tokenizer = get_tokenizer()


def merge_locations(locs, text):
    """Merges all words in locs list that are spaced at most two characters
    apart in text. (i.e. ", "). Assumes locs are in order in text.
    """
    idx = 0
    last_idx = len(locs) - 1
    merged = []
    while idx <= last_idx:
        loc = locs[idx]
        while not idx is last_idx:
            # "Trims" the text after looking at each location to prevent
            # indexing the wrong occurence of the location word if it
            # occurs multiple times in the text.
            gap, text, merge = gap_length(locs[idx], locs[idx + 1], text)
            if gap <= 2:
                loc += merge
                idx += 1
            else:
                break
        merged.append(loc)
        idx += 1
    return merged


def gap_length(word1, word2, text):
    """Returns the number of characters after the end of word1 and
    before the start of word2 in text. Also returns the "trimmed"
    text with whitespace through word1's position and the
    merged words expression.
    """
    pos1, pos2 = text.index(word1), text.index(word2)
    pos1_e, pos2_e = pos1 + len(word1), pos2 + len(word2)
    gap = pos2 - pos1_e

    # Substitute characters already looked at with whitespace
    edited_text = chr(0) * pos1_e + text[pos1_e:]
    inter_text = text[pos1_e:pos2_e]
    return gap, edited_text, inter_text


def extract_from_file(activity_file, document_file, doc_reader=Pdfreader):
    classifier = get_trained_classifier()
    reader = doc_reader(document_file)
    reader.read()
    tagged_locations = []
    for p in reader.get_pages_text():

        sentences = sentence_tokenizer.tokenize(p.encode("ascii", "ignore"))

        for sentence in sentences:
            sentence = sentence.replace('\n', '')
            #print (sentence)
            tokenized_text = word_tokenizer.tokenize(sentence)
            features = bag_of_words(tokenized_text)

            if classifier.classify(bag_of_words(tokenized_text)) == 'geography':
                tagged = tagger.get_entities(sentence)
                locs = [(word) for word, tag in tagged if tag in ['LOCATION']]
                if len(locs) > 0:
                    merged = merge_locations(locs, sentence)
                    for loc in merged:
                        tagged_locations.append((loc, sentence))

    return tagged_locations




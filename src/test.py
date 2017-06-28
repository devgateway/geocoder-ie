import nltk

from sner import Ner
tagger = Ner(host='localhost', port=9000)

sentence_tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')

text="this is is a test in London"

print (tagger.get_entities(sentence_tokenizer.tokenize(text)[0]))
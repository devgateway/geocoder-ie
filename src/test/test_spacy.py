import spacy
from spacy.lang.fr.examples import sentences

nlp = spacy.load('fr_core_news_sm')
doc = nlp(sentences[0])
print(doc.text)
for token in doc:
    print(token.text, token.pos_, token.dep_)
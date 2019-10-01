import nltk
from nltk.stem.snowball import FrenchStemmer
from nltk.corpus import stopwords
import re
from collections import Counter
from nltk.tokenize import word_tokenize

import json


def test():
    content_french = [
        "Les astronomes amateurs jouent également un rôle important en recherche. Sérieux participant couramment au suivi d'étoiles variables, à la découverte de nouveaux astéroïdes et de nouvelles comètes, etc.",
        'Séquence vidéo.', "John Richard Bond explique le rôle de l'astronomie."]
    tokenizer = nltk.data.load('tokenizers/punkt/PY3/french.pickle')
    for i in content_french:
        print(i)
        print(tokenizer.tokenize(i))


if __name__ == '__main__':
    print("Hello")
    test()


def parseJson(text):
    jo = json.load(text)
    return jo


# -*- coding: utf-8 -*-
import os
from nltk import FreqDist, ConditionalFreqDist, LaplaceProbDist, ELEProbDist
from nltk.classify.util import accuracy
from nltk.classify.naivebayes import NaiveBayesClassifier
from nltk.collocations import BigramCollocationFinder
from nltk.corpus import stopwords
from nltk.corpus.reader import PlaintextCorpusReader, CategorizedPlaintextCorpusReader
from nltk.metrics.association import BigramAssocMeasures
import collections
from nltk.tokenize import word_tokenize

__author__ = 'sebas'

english_stops = set(stopwords.words('english'))
corpora_path = os.path.join(os.path.dirname(__file__),'../../corpora/categorized/')
corpus = CategorizedPlaintextCorpusReader(corpora_path, r'(?!\.).*\.txt', cat_pattern=r'(none|geography)/.*', encoding='ISO-8859-1')

documents = [(list(corpus.words(fileid)), category) for category in corpus.categories() for fileid in
             corpus.fileids(category)]

def bag_of_words(words):
    return dict(
        [('contains(%s)' % word.lower(), True) for word in words if word not in english_stops and len(word) > 3])


def bag_of_words_in_set(words, goodwords):
    return bag_of_words(set(words) & set(goodwords))


def bag_of_bigrams_words(words, score_fn=BigramAssocMeasures.chi_sq, n=200):
    bigrams = BigramCollocationFinder.from_words(words).nbest(score_fn, n)
    return bag_of_words(words + bigrams)


def label_feats_from_corpus(corp, feature_detector=bag_of_words):
    label_feats = collections.defaultdict(list)
    for label in corp.categories():
        for fileid in corp.fileids(categories=[label]):
            feats = feature_detector(corp.words(fileids=[fileid]))
            label_feats[label].append(feats)
    return label_feats


def split_label_feats(lfeats, split=0.75):
    train_feats = []
    test_feats = []
    for label, feats in lfeats.items():
        cutoff = int(len(feats) * split)
        train_feats.extend([(feat, label) for feat in feats[:cutoff]])
        test_feats.extend([(feat, label) for feat in feats[cutoff:]])
    return train_feats, test_feats


def high_information_words(labelled_words, score_fn=BigramAssocMeasures.chi_sq, min_score=5):
    word_fd = FreqDist()
    label_word_fd = ConditionalFreqDist()
    for label, words in labelled_words:
        for word in words:
            word_fd[word] += 1
            label_word_fd[label][word] += 1

    n_xx = label_word_fd.N()
    high_info_words = set()

    for label in label_word_fd.conditions():
        n_xi = label_word_fd[label].N()
        word_scores = collections.defaultdict(int)

    for word, n_ii in label_word_fd[label].items():
        n_ix = word_fd[word]
        score = score_fn(n_ii, (n_ix, n_xi), n_xx)
        word_scores[word] = score
        bestwords = [word for word, score in word_scores.items() if score >= min_score]
        high_info_words |= set(bestwords)

    return high_info_words


def get_trained_classifier():
    lfeats = label_feats_from_corpus(corpus)
    train_feats, test_feats = split_label_feats(lfeats)
    nb_classifier = NaiveBayesClassifier.train(train_feats, estimator=ELEProbDist)
    print accuracy(nb_classifier, test_feats)
    nb_classifier.show_most_informative_features(n=20)
    return nb_classifier


def test():
    nb_classifier = get_trained_classifier();
    print(nb_classifier.classify(bag_of_words(word_tokenize("""districts inhabitants highways and """.lower()))))
    print(nb_classifier.classify(bag_of_words(word_tokenize("""covers 32 districts""".lower()))))
    print(nb_classifier.classify(bag_of_words(word_tokenize("""Country Argentina with 32 districts """.lower()))))
    print(nb_classifier.classify(bag_of_words(word_tokenize("""The capital city of argentina is Buenos Aires""".lower()))))

import nltk
from nltk.corpus.reader.plaintext import PlaintextCorpusReader,\
    CategorizedPlaintextCorpusReader
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag

cor= CategorizedPlaintextCorpusReader('../classifier/', r'(?!\.).*\.txt', cat_pattern=r'(geography|sectors|cost)/.*', encoding='utf-8')

documents = [(list(cor.words(fileid)), category)
              for category in cor.categories()
              for fileid in cor.fileids(category)]




all_words = nltk.FreqDist(w.lower() for w in cor.words())

word_features = list(all_words)[:50]



def sentence_features(text): 
    document_words = set(text) 
    features = {}
    for word in word_features:
        features['contains({})'.format(word)] = (word in document_words)
    return features




featuresets = [(sentence_features(d), c) for (d,c) in documents]

train_set, test_set = featuresets, featuresets

classifier = nltk.NaiveBayesClassifier.train(train_set)
classifier.show_most_informative_features(5)


print  classifier.classify(sentence_features(word_tokenize(u'The project will be financed')))
print  classifier.classify(sentence_features(word_tokenize(u'The project Location')))
print  classifier.classify(sentence_features(word_tokenize(u'project region is')))
print  classifier.classify(sentence_features(word_tokenize(u'sector')))





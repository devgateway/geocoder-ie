import numpy
from sklearn.metrics.classification import confusion_matrix, f1_score, recall_score, precision_score
from sklearn.model_selection._split import KFold, train_test_split
from dg.geocoder.classification.classifier import Classifier
from dg.geocoder.classification.plot import plot_confusion_matrix


class Trainer:
    def __init__(self, data, classifier=Classifier()):
        self.cls = classifier
        self.data = data
        self.raw_texts = data['text'].values
        self.values = data['class'].values
        self.score = 0.0
        self.recall = 0.0
        self.precision = 0.0
        self.confusion = numpy.array([[0, 0], [0, 0]])

    def _get_train_test_sets(self):
        X_train, X_test, Y_train, Y_test = train_test_split(self.raw_texts, self.values, test_size=0.3, random_state=0)

        return X_train, X_test, Y_train, Y_test

    def split_train(self):
        X_train, X_test, Y_train, Y_test = self._get_train_test_sets()
        # fit classifier with train set and train labels
        self.cls.train(X_train, Y_train)

        # collect prediction for scoring purpose
        predictions = self.cls.predict(X_test)
        self.recall = recall_score(Y_test, predictions, pos_label='geography')
        self.precision = precision_score(Y_test, predictions, pos_label='geography')
        self.score = f1_score(Y_test, predictions, pos_label='geography')
        self.confusion += confusion_matrix(Y_test, predictions)

        return self.cls

    def kfold_train(self, n_splits=3):
        print('train classifier using kFold')
        kf = KFold(n_splits=n_splits, shuffle=True)
        scores = []
        precisions = []
        recalls = []
        for train_index, test_index in kf.split(self.data):
            train_text = self.data.iloc[train_index]['text'].values
            train_y = self.data.iloc[train_index]['class'].values

            test_text = self.data.iloc[test_index]['text'].values
            test_y = self.data.iloc[test_index]['class'].values

            self.cls.train(train_text, train_y)
            predictions = self.cls.predict(test_text)
            self.confusion += confusion_matrix(test_y, predictions)
            scores.append(f1_score(test_y, predictions, pos_label='geography'))
            recalls.append(recall_score(test_y, predictions, pos_label='geography'))
            precisions.append(precision_score(test_y, predictions, pos_label='geography'))

        self.score = sum(scores) / len(scores)
        self.precision = sum(precisions) / len(precisions)
        self.recall = sum(recalls) / len(recalls)

        return self.cls

    def get_classifier(self):
        return self.cls

    def print_stats(self):
        print('Total classified:', len(self.data))
        print('Score:', self.score)
        print('Precision:', self.precision)
        print('Recall:', self.recall)
        print('Confusion matrix:')
        print(self.confusion)

    def plot_stats(self):
        plot_confusion_matrix(self.confusion, ['geography', 'none'])

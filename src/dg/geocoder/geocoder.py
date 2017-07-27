from dg.geocoder.classification.classifier import load_classifier


def process_activity(activity):
    print(activity)


def bulk_process(xml, path_to_docs='docs'):
    if xml is None:
        print('xml file should be provide')
    else:
        print('Process list of activities')


def classify_document(file, cls_name='default_classifier'):
    classifier = load_classifier(cls_name)




if __name__ == '__main__':
    classify_document(None,cls_name='sebas')


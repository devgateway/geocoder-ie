# -*- coding: utf-8 -*-
import os
from prettytable import PrettyTable
from extraction.locations_extractor import extract_from_file
from iati.iati_downloader import activity_data_download

__author__ = 'sebas'

corpora = ''

dir = os.path.dirname(__file__)

samples = [
    os.path.join(dir,
                 '../corpora/projects/AFDB/guinea/46002-P-GN-DB0-005/Guinea_-_Tombo-Gbessia_Road_Improvement_Project_-_Appraisal_Report.pdf'),
    os.path.join(dir,
                 '../corpora/projects/AFDB/zimbabwe/46002-P-ZW-DB0-005/Zimbabwe_-_National_Transport_Sector_Master_Plan_Study_-_Appraisal_Report.pdf'),
    os.path.join(dir,
                 '../corpora/projects/AFDB/zimbabwe/46002-P-ZW-E00-003/Zimbabwe_-_Urgent_Water_Supply_and_Sanitation_Rehabilitation_Project_-_Phase_2_-_Appraisal_Report.pdf'),
    os.path.join(dir, '../corpora/projects/AFDB/south_africa/46002-P-ZA-B00-001/ESIA%20summary%20Kalagadi.pdf'),
    os.path.join(dir,
                 '../corpora/projects/AFDB/south_africa/46002-P-ZA-F00-002/ESIA_Summary_Eskom%20Renewable%20Energy%20Investment%20Project_%20FINAL_%20July%202010.pdf')
]

activity_samples = ["46002-P-GN-DB0-005", "46002-P-ZW-E00-003", "46002-P-ZA-B00-001"]


# os.system( 'java -mx400m -cp ../stanford-ner-2016-10-31/stanford-ner.jar edu.stanford.nlp.ie.NERServer -loadClassifier ../stanford-ner-2016-10-31/classifiers/english.all.3class.distsim.crf.ser.gz -port 1234 ')

import re


def find_in_text(word, text):
    for m in re.finditer(re.escape(word), text):
        yield (word, m.start(), m.end())




def auto_geocode(identifier):
    # downlaod activity data
    table = PrettyTable(['Location', 'Sentence'])
    table.align= "l"
    activity_files = activity_data_download(identifier)
    for doc in activity_files[1]:
        results = extract_from_file(activity_files[0], doc)
        for r in results:
            try:
                table.add_row([r[0], r[1][0:100]])
            except ValueError:
                print 'Error'
        print (table)

            # for id in activity_samples:


if __name__ == "__main__":
    import sys
    print (sys.argv)
    if len(sys.argv) > 1:
        auto_geocode(sys.argv[1])
    else:
        print('Please provide a IATI activity identifier')


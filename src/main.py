import os
from extraction.locations_extractor import extract_from_file
from iati.activity_reader import ActivityReader
from iati.iati_downloader import activity_data_download

__author__ = 'sebas'

corpora = ''

dir = os.path.dirname(__file__)

samples = [
    os.path.join(dir,'../corpora/projects/AFDB/guinea/46002-P-GN-DB0-005/Guinea_-_Tombo-Gbessia_Road_Improvement_Project_-_Appraisal_Report.pdf'),
    os.path.join(dir,'../corpora/projects/AFDB/zimbabwe/46002-P-ZW-DB0-005/Zimbabwe_-_National_Transport_Sector_Master_Plan_Study_-_Appraisal_Report.pdf'),
    os.path.join(dir,'../corpora/projects/AFDB/zimbabwe/46002-P-ZW-E00-003/Zimbabwe_-_Urgent_Water_Supply_and_Sanitation_Rehabilitation_Project_-_Phase_2_-_Appraisal_Report.pdf'),
    os.path.join(dir, '../corpora/projects/AFDB/south_africa/46002-P-ZA-B00-001/ESIA%20summary%20Kalagadi.pdf'),
    os.path.join(dir,'../corpora/projects/AFDB/south_africa/46002-P-ZA-F00-002/ESIA_Summary_Eskom%20Renewable%20Energy%20Investment%20Project_%20FINAL_%20July%202010.pdf')
]



activity_samples = ["46002-P-GN-DB0-005", "46002-P-ZW-E00-003", "46002-P-ZA-B00-001"]


def auto_geocode(identifier):
    # downlaod activity data
    activity_files = activity_data_download(identifier)
    for doc in activity_files[1]:
        results = extract_from_file(activity_files[0], doc)
        for r in results:
            print(r[0])

for id in activity_samples:
    auto_geocode(id)

# -*- coding: utf-8 -*-
import re
import json
from prettytable import PrettyTable
from extraction.locations_extractor import extract_from_file
from gazetteer.geonames import geonames_query, lookup_locations
import csv
from iati.iati_downloader import activity_data_download


__author__ = 'sebas'

def find_in_text(word, text):
    for m in re.finditer(re.escape(word), text):
        yield (word, m.start(), m.end())


def auto_geocode(identifier):
    # downlaod activity data
    table = PrettyTable(['Location','Sentence'])
    table.align= "l"
    activity_files = activity_data_download(identifier)
    for doc in activity_files[1]:
        results = extract_from_file(activity_files[0], doc)
        locations=[(loc) for loc,text in results]
        #geocoded=lookup_locations(locations)
        for r in results:
            try:
                table.add_row([r[0],r[1][0:120]])
            except ValueError:
                print 'Error'

        print(table)

        print ('')
        print ('Sebas you have to open results.csv file now!'.upper())
        print ('')


def writeCsv(geocoded):
    with open('results.csv', 'wb') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=',',
                                quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for (key) in geocoded:
            try:
                spamwriter.writerow([geocoded[key]['name'],geocoded[key]['fcodeName'],geocoded[key]['lat'],geocoded[key]['lon']])
            except:
                pass


def toGeoJson(geocoded):
    features=[]
    for (key) in geocoded:
        try:
            feature= {
                "type": "Feature",
                "geometry": {
                    "type": "Point",
                    "coordinates": [geocoded[key]['lat'], geocoded[key]['lon']]
                },
                "properties": {
                    "name": geocoded[key]['name'],
                    "fcodeName":geocoded[key]['fcodeName']
                }
            }
            features.append(features)
        except:
            pass

        print(json.dumps(features))


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        auto_geocode(sys.argv[1])
    else:
        print('Please provide a IATI activity identifier')


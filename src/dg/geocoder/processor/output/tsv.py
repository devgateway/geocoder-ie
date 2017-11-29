import csv
import logging.config
import os

from dg.geocoder.config import get_log_config_path

logging.config.fileConfig(get_log_config_path())
logger = logging.getLogger()


# Save results to TSV
def save_to_tsv(out_file, geocoding, out_path=''):
    try:
        with open(os.path.realpath(os.path.join(out_path, out_file)), 'w+', newline='') as csvfile:
            fieldnames = ['geonameId', 'name', 'toponymName', 'fcl', 'fcode', 'fcodeName', 'fclName', 'lat', 'lng',
                          'adminCode1', 'adminName1', 'adminCode2', 'adminName2', 'adminCode3', 'adminName3',
                          'adminCode4',
                          'adminName4', 'countryName', 'population', 'continentCode', 'countryCode',
                          ]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter='\t', quotechar='"',
                                    quoting=csv.QUOTE_MINIMAL)
            writer.writeheader()
            for data, text in geocoding:
                writer.writerow(data)
        csvfile.close()
        return out_file
    except Exception as e:
        logger.error('Error while writing tsv file {}'.format(e))
        raise

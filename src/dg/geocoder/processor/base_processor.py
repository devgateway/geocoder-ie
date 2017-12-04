import csv
import json
import logging.config
import os

from dg.geocoder.config import get_log_config_path
from dg.geocoder.model.models import get_activity_dict, get_location_dic

logging.config.fileConfig(get_log_config_path())
logger = logging.getLogger()

ST_PROCESSING = "PROCESSING"
ST_PROCESSED = "PROCESSED"
ST_PENDING = "PENDING"
ST_ERROR = "ERROR"
FORMAT_TSV = 'tsv'
FORMAT_XML = 'xml'
FORMAT_JSON = 'json'


class BaseProcessor:
    def __init__(self, *args, **kwargs):
        self.results = []
        self.locations = []
        self.cty_codes = kwargs.get("cty_codes", [])
        self.step_logger = kwargs.get("step_logger", None)

    def process(self):
        pass

    def get_locations(self):
        return self.locations

    def get_results(self):
        return self.results

    def write_output(self, out_format=FORMAT_TSV, out_path='', out_file='out'):
        if out_format == FORMAT_TSV or out_format is None:
            return self.save_to_tsv(out_file, self.locations, out_path=out_path)
        if out_format == FORMAT_JSON:
            return self.save_to_json(out_file, self.locations, out_path=out_path)
        if out_format == FORMAT_XML:
            logger.error("The output format is not supported fot the provided input file")

    def save_output(self):
        pass

    @staticmethod
    def save_to_tsv(out_file, geocoding, out_path=''):
        try:
            out_file_with_extension = '{}.tsv'.format(out_file)
            with open(os.path.realpath(os.path.join(out_path, out_file_with_extension)), 'w+', newline='') as csvfile:
                fieldnames = ['geonameId', 'name', 'toponymName', 'fcl', 'fcode', 'fcodeName', 'fclName', 'lat', 'lng',
                              'adminCode1', 'adminName1', 'adminCode2', 'adminName2', 'adminCode3', 'adminName3',
                              'adminCode4',
                              'adminName4', 'countryName', 'population', 'continentCode', 'countryCode',
                              ]
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter='\t', quotechar='"',
                                        quoting=csv.QUOTE_MINIMAL)
                writer.writeheader()
                id, locations = geocoding[0]
                for data in locations:
                    writer.writerow(data)
            csvfile.close()
            return out_file_with_extension
        except Exception as e:
            logger.error('Error while writing tsv file {}'.format(e))
            raise

    @staticmethod
    def save_to_json(out_file, activities_locations, out_path=''):
        try:
            out_file_with_extension = '{}.json'.format(out_file)

            json_data = []
            for id, locations in activities_locations:
                json_data.append(get_activity_dict(id, get_location_dic(locations)))

            with open(out_file_with_extension, 'w') as f:
                json.dump(json_data, f, ensure_ascii=False, indent=4)

            f.close()
            return out_file_with_extension
        except Exception as e:
            logger.error('Error while writing json file {}'.format(e))
            raise

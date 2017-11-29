import json
import logging.config

from dg.geocoder.config import get_log_config_path
from dg.geocoder.model.models import get_activity_dict, get_location_dic

logging.config.fileConfig(get_log_config_path())
logger = logging.getLogger()


def save_to_json(out_file, activities_locations, out_path=''):
    try:
        json_data = []
        for id, locations in activities_locations:
            json_data.append(get_activity_dict(id, get_location_dic(locations)))

        with open(out_file, 'w') as f:
            json.dump(json_data, f, ensure_ascii=False, indent=4)

        f.close()
        return out_file
    except Exception as e:
        logger.error('Error while writing json file {}'.format(e))
        raise

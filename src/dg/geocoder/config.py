import os
from configparser import ConfigParser

import dg as main_package

app_root_path = os.path.realpath(os.path.join(os.path.dirname(main_package.__file__), '..', '..', ))

app_config_file_path = os.path.realpath(os.path.join(app_root_path, 'geocoder.ini'))

parser = ConfigParser()
parser.read(app_config_file_path)


def get_ner_host():
    return parser.get('standford', 'host')


def get_ner_port():
    return int(parser.get('standford', 'port'))


def get_geonames_base_url():
    return parser.get('geonames', 'baseurl')


def get_geonames_user_name():
    return parser.get('geonames', 'username')


def get_ignore_entities():
    return parser.get('ie', 'ignore_entities').lower().split(' ')


def get_ignore_gap_chars():
    return parser.get('ie', 'ignore_gap_chars').lower().split(' ')


def get_classifiers_path():
    return os.path.realpath(os.path.join(app_root_path, parser.get('fs', 'classifiers_path')))


def get_db_name():
    return parser.get('postgres', 'db_name')


def get_user_name():
    return parser.get('postgres', 'user_name')


def get_password():
    return parser.get('postgres', 'password')


def get_download_path():
    return os.path.realpath(os.path.join(app_root_path, parser.get('fs', 'download_path')))


def get_iati_xsd_path():
    return os.path.realpath(os.path.join(app_root_path, parser.get('fs', 'iati_xsd_path')))


def get_activities_xsd_file_path(version):
    target = os.path.realpath(os.path.join(get_iati_xsd_path(), version, 'iati-activities-schema.xsd'))
    if not os.path.exists(target):
        raise IOError("Wasn't able to find xsd file for version {}".format(version))
    else:
        return target

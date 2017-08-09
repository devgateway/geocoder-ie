from configparser import ConfigParser

parser = ConfigParser()
parser.read('geocoder.ini')


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
    return parser.get('fs', 'classifiers_path')


def get_db_name():
    return parser.get('postgres', 'db_name')


def get_user_name():
    return parser.get('postgres', 'user_name')


def get_password():
    return parser.get('postgres', 'password')



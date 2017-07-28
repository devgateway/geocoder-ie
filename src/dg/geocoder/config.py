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

from configparser import ConfigParser

parser = ConfigParser()
parser.read('geocoder.ini')


def get_ner_host():
    return parser.get('standford', 'host')


def get_ner_port():
    return int(parser.get('standford', 'port'))

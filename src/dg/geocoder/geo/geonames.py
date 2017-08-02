import json
from urllib.error import URLError
from urllib.request import urlopen

from dg.geocoder.config import get_geonames_base_url, get_geonames_user_name


def query(location, country_code):
    baseurl = get_geonames_base_url()
    username = get_geonames_user_name()
    json_decode = json.JSONDecoder()  # used to parse json response

    try:
        ##combine all variables into query string
        # query_string = baseurl+'username=%s&name_equals=%s&north=%s&south=%s&east=%s&west=%s&orderby=population' % (username,location,north,south,east,west)
        # query_string = baseurl + 'username=%s&name_equals=%s&orderby=relevance' % (username, location)
        ##run query, read output, and parse json response

        query_string = baseurl + 'username=%s&name_equals=%s&orderby=population' % (
            username, location, north, south, east, west)

        response = urlopen(query_string)
        response_string = response.read()
        parsed_response = json_decode.decode(response_string)
        # check to make sure there is a response to avoid keyerror
        if len(parsed_response['geonames']) > 0:
            first_response = parsed_response['geonames'][0]
            data = {'lat': first_response['lat'],
                    'lon': first_response['lng'],
                    'fcodeName': first_response['fcodeName'],
                    'name': first_response['name']
                    }

        else:
            data = {}
    except URLError as e:
        data = {}

    return data


def lookup_locations(locations):
    location_names = [x for x in locations]  # separate names from index
    '''given list of locations, run query for each and return dict'''
    coordinates = {}  # dict to store coordinates
    all_locations = dict({})
    unique_locs = list(set(location_names))  # only look up locations once
    # get coordinates for every unique location
    for place in unique_locs:
        data = query(place)
        all_locations[place] = data

    return all_locations

import json
import logging
from urllib.error import URLError
from urllib.request import urlopen

from requests.utils import quote

from dg.geocoder.config import get_geonames_base_url, get_geonames_user_name, get_geonames_retry_policy

logger = logging.getLogger()


def parse(data):
    return {
        'toponymName': data.get('toponymName', ''),
        'name': data.get('name', ''),
        'lat': data.get('lat', ''),
        'lng': data.get('lng', ''),
        'geonameId': data.get('geonameId', ''),
        'countryCode': data.get('countryCode', ''),
        'countryName': data.get('countryName', ''),
        'fcl': data.get('fcl', ''),
        'fcode': data.get('fcode', ''),
        'fclName': data.get('fclName', ''),
        'fcodeName': data.get('fcodeName', ''),
        'population': data.get('population', ''),
        'continentCode': data.get('continentCode', ''),
        'adminCode1': data.get('adminCode1', ''),
        'adminName1': data.get('adminName1', ''),
        'adminCode2': data.get('adminCode2', ''),
        'adminName2': data.get('adminName2', ''),
        'adminCode3': data.get('adminCode3', ''),
        'adminName3': data.get('adminName3', ''),
        'adminCode4': data.get('adminCode4', ''),
        'adminName4': data.get('adminName4', '')
    }


def get_by_priority(results):
    if len(results) > 0:
        priorities = ['PCLI', 'ADM1', 'ADM2', 'ADM3', 'ADM4', 'ADM5', 'RGN', 'RGNE', 'RGNH', 'PPL', 'PPLA', 'PPLA2',
                      'PPLA3', 'PPLA4', 'PPLL']
        locations = []
        for l in results:  # iterate locations
            f_code = l.get('fcode')
            # if f_code is equ to current priority return
            for idx, p in enumerate(priorities):
                if f_code == p:
                    locations.append((idx, l))
                    pass

            locations.sort(key=lambda x: x[0])
        # return element that got in first order
        if len(locations) > 0:
            return locations[0][1]
    else:
        return None


def resolve(loc, cty_codes, rels=None, query_method='name_equals', fuzzy=.9, retry=get_geonames_retry_policy()):
    if rels is None:
        rels = []
    selected_loc = None
    if len(loc) > 3:
        locations = query(loc, cty_codes, query_method, fuzzy)
        selected_loc = get_by_priority(locations)

        if selected_loc is None and len(locations) > 0:
            selected_loc = locations[0]

        if selected_loc:
            logger.info(
                '{} was geocode as {} with coordinates {},{}'.format(loc, selected_loc['fcode'], selected_loc['lat'],
                                                                     selected_loc['lng']))
        else:
            logger.info("Wasn't able to geocode  {}".format(loc))
            if retry:
                logger.info("Let's try using others parameters".format(loc))
                selected_loc = resolve(loc, cty_codes, rels, query_method='name', fuzzy=1, retry=False)
    else:
        logger.info('{} Too short location name'.format(loc))

    return selected_loc


def query(location, cty_codes, query_method, fuzzy):
    results = []
    try:
        base_url = get_geonames_base_url()
        username = get_geonames_user_name()
        query_string = base_url + 'username={user}&{query_method}={name}&' \
                                  'style=FULL&orderby={order}&startRow=0&maxRows=5&fuzzy={fuzzy}' \
            .format(user=username, query_method=query_method, name=quote(location), order='relevance', fuzzy=fuzzy)
        if cty_codes and len(cty_codes) > 0:
            query_string = query_string + '&' + '&'.join([('country={}'.format(c)) for c in cty_codes])

        json_decode = json.JSONDecoder()  # used to parse json response
        response = urlopen(query_string)
        # logger.info("Querying geoname {}".format(query_string))
        response_string = response.read().decode('utf-8')
        parsed_response = json_decode.decode(response_string)
        if parsed_response.get('geonames') and len(parsed_response.get('geonames')) > 0:
            for item in parsed_response['geonames']:
                results.append(parse(item))

    except URLError as e:
        logger.info("Oops!  something didn't go well")
        logger.info(e)

    return results

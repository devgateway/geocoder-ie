import json
from urllib.error import URLError
from urllib.request import urlopen

from requests.utils import quote

from dg.geocoder.config import get_geonames_base_url, get_geonames_user_name


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
        'adminName4': data.get('adminName4', ''),
        'timezone': data.get('timezone', '')
    }


def importance_3(results):
    for l in results:
        f_code = l.get('fcode')
        if f_code in ['PPL', 'PPLA', 'PPLA2', 'PPLA3', 'PPLA4', 'PPLL']:
            return l

    return None


def importance_2(results):
    for l in results:
        f_code = l.get('fcode')
        if f_code in ['RGN', 'RGNE', 'RGNH']:
            return l

    return None


def importance_1(results):
    for l in results:
        f_code = l.get('fcode')
        if f_code in ['ADM1', 'ADM2', 'ADM3', 'ADM4', 'ADM5']:
            return l

    return None


# this method should return a single location
def resolve(loc, cty_codes, rels=[]):
    locations = query(loc, cty_codes)

    selected_loc = importance_1(locations)

    if selected_loc is None:
        selected_loc = importance_2(locations)
    if selected_loc is None:
        selected_loc = importance_3(locations)

    if selected_loc is None and len(locations) > 0:
        selected_loc = locations[0]

    if selected_loc:
        print('{} was geocode as {} with coordinates {},{}'.format(loc, selected_loc['fcode'], selected_loc['lat'],
                                                                   selected_loc['lng']))
    else:
        print("{} wasn't geocoded :( ".format(loc))

    return selected_loc


def query(location, cty_codes):
    results = []

    try:
        base_url = get_geonames_base_url()
        username = get_geonames_user_name()
        query_string = base_url + 'username={user}&name_equals={name}&style=FULL&orderby={order}&startRow=0&maxRows=5&fuzzy=.9' \
            .format(user=username, name=quote(location), order='relevance')

        if cty_codes and len(cty_codes) > 0:
            query_string = query_string + '&' + '&'.join([('country={}'.format(c)) for c in cty_codes])

        json_decode = json.JSONDecoder()  # used to parse json response
        response = urlopen(query_string)
        response_string = response.read().decode('utf-8')
        parsed_response = json_decode.decode(response_string)
        if len(parsed_response['geonames']) > 0:
            for item in parsed_response['geonames']:
                results.append(parse(item))

    except URLError as e:
        print("Oops!  something didn't go well")
        print(e)

    return results

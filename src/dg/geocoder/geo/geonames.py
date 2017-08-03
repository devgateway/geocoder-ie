import json
from urllib.error import URLError
from urllib.request import urlopen

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


# this method should return a single location
def search(name, country_codes=[], rels=[]):
    results = []

    if len(rels) > 0:
        for r in rels:
            results = query('{0} {1}'.format(name, r), mode='q')

    print('.............looking for {}.........'.format(name))
    if (len(results) > 0):
        # non single results, let's see if we can reduce it
        for loc in results[0:10]:
            adm1 = loc.get('adminName1')
            adm2 = loc.get('adminName2')
            adm3 = loc.get('adminName3')
            adm4 = loc.get('adminName4')
            print('{} {} {} {} '.format(adm1, adm2, adm3, adm4))
    return results


def query(location, country_codes=None, mode='equals_name'):
    results = []
    try:
        baseurl = get_geonames_base_url()
        username = get_geonames_user_name()
        query_string = baseurl + 'username={user}&equals_name={name}&style=FULL&orderby={order}'.format(
            user=username,
            name=location,
            order='population')
        if country_codes and len(country_codes) > 0:
            query_string = query_string + '&' + '&'.join([('country={}'.format(c)) for c in country_codes])

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

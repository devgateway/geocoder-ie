import json
import urllib2

def other():
    print ('other')


def geonames_query(location,east='-74.803504',west='-75.413986',north='40.186939',south='39.816113'):
    baseurl = 'http://api.geonames.org/searchJSON?' #baseurl for geonames
    username = 'prpole' #make a geonames username
    json_decode = json.JSONDecoder() #used to parse json response

    #use try/except to catch timeout errors
    try:
        ##combine all variables into query string
        #query_string = baseurl+'username=%s&name_equals=%s&north=%s&south=%s&east=%s&west=%s&orderby=population' % (username,location,north,south,east,west)
        query_string = baseurl+'username=%s&name_equals=%s&orderby=relevance' % (username,location)
        ##run query, read output, and parse json response
        response = urllib2.urlopen(query_string)
        response_string = response.read()
        parsed_response = json_decode.decode(response_string)
        #check to make sure there is a response to avoid keyerror
        if len(parsed_response['geonames']) > 0:
            first_response = parsed_response['geonames'][0]
            data = {'lat':first_response['lat'],
                    'lon':first_response['lng'],
                    'fcodeName':first_response['fcodeName'],
                    'name':first_response['name']
            }

        else:
            data = {}
    except urllib2.URLError as e:
        data = {}

    return data

def lookup_locations(locations):
    location_names = [ x for x in locations ] #separate names from index
    '''given list of locations, run query for each and return dict'''
    coordinates = {} #dict to store coordinates
    all_locations = dict({})
    unique_locs = list(set(location_names)) #only look up locations once
    #get coordinates for every unique location
    for place in unique_locs:
        data = geonames_query(place)
        all_locations[place]=data

    return all_locations





#print(lookup_locations(['Cordoba'],"Cordoba'"))
import logging

from fuzzywuzzy import fuzz

logger = logging.getLogger()


def get_admin_level(level):
    if level == 'PCLI':
        return 'ADM0'

    return level


# to identify if we can return the match result of fuzzy search
def get_match_result_by_name(geoname, amp_location):
    return fuzz.token_sort_ratio(amp_location["name"].lower(), geoname["name"].lower())


def get_match_result_by_admin_level(geoname, amp_location):
    if amp_location["admin_level_code"] == get_admin_level(geoname["fcode"]):
        return 1
    return 0


def get_match_result_by_geocode_id(geoname, amp_location):
    if amp_location["geo_code"] == str(geoname["geoname_id"]):
        return 1
    return 0


# Get matched results as a tuple. The values are
# [0] - the matched value by geocode id. Possible values: 0 - unmatched, 1 - matched
# [1] - the matched value by admin_level. Possible values: 0 - unmatched, 1 - matched
# [2] - the matched value by name. Possible value between 0 and 100, depending of the fuzzy search matching
def get_matched_result(geoname, amp_location):
    return get_match_result_by_geocode_id(geoname, amp_location), \
           get_match_result_by_admin_level(geoname, amp_location), \
           get_match_result_by_name(geoname, amp_location)


def is_matched_result_valid(result):
    if result is None or result == (0, 0, 0):
        return False

    if result[0] == 0 and result[2] < 90:
        return False

    return True


def get_matched_amp_locations(geonames, amp_locations):
    matched_location_results = []

    for geoname in geonames:
        for location in amp_locations:
            matched_location_result = get_matched_result(geoname, location)

            if is_matched_result_valid(matched_location_result):
                matched_location_results.append((location, matched_location_result))

    matched_location_results.sort(key=lambda tup: (tup[1][0], tup[1][1], tup[1][2]), reverse=True)

    if len(matched_location_results) > 0:
        return [loc[0] for loc in matched_location_results]

    return None

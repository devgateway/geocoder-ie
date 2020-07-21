import unittest

from dg.geocoder.amp.amp_location_matcher import get_matched_amp_locations
from dg.geocoder.geo.geonames import resolve, resolve_all

amp_locations = [{"name": "Jacmel", "amp_location_id": 2, "admin_level_code": "ADM1",
                  "geo_code": "3723781", "gs_lat": "18.47468", "gs_long": "-72.3366"},
                 {"name": "Haiti", "amp_location_id": 1, "admin_level_code": "ADM0",
                  "geo_code": "3723782", "gs_lat": "18.2956844005", "gs_long": "-72.5208319285"},
                 {"name": "Arrondissement de Port-au-Prince Haiti", "amp_location_id": 3, "admin_level_code": "ADM2",
                  "geo_code": "3723783", "gs_lat": "18.2956844005", "gs_long": "-72.5208319285"},
                 {"name": "Port-au-Prince", "amp_location_id": 4, "admin_level_code": "ADM3",
                  "geo_code": "3723784", "gs_lat": "18.2956844005", "gs_long": "-72.5208319285"}]


def contains_location_id(amp_matched_locations, id):
    return id in [loc['amp_location_id'] for loc in amp_matched_locations];


class TestGeonameAmpLocationMatcher(unittest.TestCase):

    def test_identical_name(self):
        geocode_locations = resolve_all('Haiti', cty_codes=['HT'])
        for geocode in geocode_locations:
            geocode["geoname_id"] = geocode["geonameId"]
        amp_matched_locations = get_matched_amp_locations(geocode_locations, amp_locations)

        assert contains_location_id(amp_matched_locations, 1), "Should be matched Haiti with amp_location_id = 1"

    def test_different_name(self):
        geocode_locations = resolve_all('Jacmel', cty_codes=['HT'])
        for geocode in geocode_locations:
            geocode["geoname_id"] = geocode["geonameId"]
        amp_matched_locations = get_matched_amp_locations(geocode_locations, amp_locations)

        assert contains_location_id(amp_matched_locations, 2), "Should be matched Jacmel with amp_location_id = 2"

    def test_same_name_different_level(self):
        geocode_locations = resolve_all('Port-au-Prince', cty_codes=['HT'])
        for geocode in geocode_locations:
            geocode["geoname_id"] = geocode["geonameId"]
        amp_matched_locations = get_matched_amp_locations(geocode_locations, amp_locations)

        assert contains_location_id(amp_matched_locations, 3),\
            "Should be matched Arrondissement de Port-au-Prince Haiti with amp_location_id = 3"
        assert contains_location_id(amp_matched_locations, 4), \
            "Should be matched Port-au-Prince with amp_location_id = 3"


if __name__ == '__main__':
    unittest.main()

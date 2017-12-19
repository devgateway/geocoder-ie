EXACTNESS_EXACT = {"code": 1, "lang": "en", "name": "Exact The designated geographic location is exact",
                   "type": "EXACTNESS"}
EXACTNESS_APPROX = {"code": 2, "lang": "en", "name": "Approximate The designated geographic location is approximate",
                    "type": "EXACTNESS"}

LOCATION_VOCABULARY_GAUL = {"code": "A1", "lang": "en", "name": "Global Admininistrative Unit Layers",
                            "type": "LOCATION_VOCABULARY"}
LOCATION_VOCABULARY_SALB = {"code": "A2", "lang": "en", "name": "UN Second Administrative Level Boundary Project",
                            "type": "LOCATION_VOCABULARY"}
LOCATION_VOCABULARY_GADMIN = {"code": "A3", "lang": "en", "name": "Global Administrative Areas",
                              "type": "LOCATION_VOCABULARY"}
LOCATION_VOCABULARY_ISO = {"code": "A4", "lang": "en", "name": "ISO Country (3166-1 alpha-2)",
                           "type": "LOCATION_VOCABULARY"}
LOCATION_VOCABULARY_GEO_NAMES = {"code": "G1", "lang": "en", "name": "Geonames", "type": "LOCATION_VOCABULARY"}
LOCATION_VOCABULARY_OSM = {"code": "G2", "lang": "en", "name": "OpenStreetMap", "type": "LOCATION_VOCABULARY"}

GAZETTEER_AGENCY_GEO_NAMES = {"type": "GAZETTEER_AGENCY", "code": "1", "lang": "en", "name": "Geonames.org"}
GAZETTEER_AGENCY_NGA = {"type": "GAZETTEER_AGENCY", "code": "2", "lang": "en",
                        "name": "National Geospatial-Intelligence Agency"}
GAZETTEER_AGENCY_OSM = {"type": "GAZETTEER_AGENCY", "code": "3", "lang": "en", "name": "Open Street Map"}

LOCATION_PRECISION_EXACT = {"type": "LOCATION_PRECISION", "code": "1", "lang": "en", "name": "Exact location"}
LOCATION_PRECISION_NEAR_EXACT = {"type": "LOCATION_PRECISION", "code": "2", "lang": "en", "name": "Near exact location"}
LOCATION_PRECISION_SECOND = {"type": "LOCATION_PRECISION", "code": "3", "lang": "en",
                             "name": "Second order administrative division"}
LOCATION_PRECISION_FIRST = {"type": "LOCATION_PRECISION", "code": "4", "lang": "en",
                            "name": "First order administrative division"}
LOCATION_PRECISION_ESTIMATED = {"type": "LOCATION_PRECISION", "code": "5", "lang": "en", "name": "Estimated coordinates"}
LOCATION_PRECISION_INDEPENDENT = {"type": "LOCATION_PRECISION", "code": "6", "lang": "en",
                                  "name": "Independent political entity"}
LOCATION_PRECISION_UNCLEAR_CAPITAL = {"type": "LOCATION_PRECISION", "code": "7", "lang": "en",
                                      "name": "Unclear - capital Unclear."}
LOCATION_PRECISION_LOCAL = {"type": "LOCATION_PRECISION", "code": "8", "lang": "en", "name": "Local or national capital"}
LOCATION_PRECISION_UNCLEAR_COUNTRY = {"type": "LOCATION_PRECISION", "code": "9", "lang": "en",
                                      "name": "Unclear - country Unclear."}
LOCATION_REACH_ACTIVITY = {"type": "LOCATION_REACH", "code": "1", "lang": "en", "name": "Activity"}
LOCATION_REACH_BENEFICIARIES = {"type": "LOCATION_REACH", "code": "2", "lang": "en",
                                "name": "Intended Beneficiaries"}

LOCATION_CLASS_ADM_REGION = {"type": "LOCATION_CLASS", "code": "1", "lang": "en", "name": "Administrative Region"}
LOCATION_CLASS_PPL = {"type": "LOCATION_CLASS", "code": "2", "lang": "en", "name": "Populated Place"}
LOCATION_CLASS_STR = {"type": "LOCATION_CLASS", "code": "3", "lang": "en", "name": "Structure"}
LOCATION_CLASS_OTHER = {"type": "LOCATION_CLASS", "code": "4", "lang": "en", "name": "Other Topographical Feature"}


def get_location_class_from_fcl(fcl):
    if fcl == 'A':
        return LOCATION_CLASS_ADM_REGION
    if fcl == 'P':
        return LOCATION_CLASS_PPL
    if fcl in ['R', 'S']:
        return LOCATION_CLASS_STR
    else:
        return LOCATION_CLASS_OTHER

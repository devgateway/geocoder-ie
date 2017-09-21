def get_location_dic(locations):
    locs = []
    for l in locations:
        locs.append({
            "name": l.get('name'),
            "id": l.get('geonameId'),
            "geometry": {
                "type": "Point",
                "coordinates": [
                    l.get('lng'),
                    l.get('lat')
                ]
            },
            "featureDesignation": {
                "code": l.get('fcode'),
                "name": l.get('fcodeName')
            },
            "country": {
                "code": l.get('countryCode'),
                "name": l.get('countryName')
            },
            "admin1": {
                "code": l.get('adminCode1'),
                "name": l.get('adminName1')
            },
            "admin2": {
                "code": l.get('adminCode2'),
                "name": l.get('adminName2')
            },
            "admin3": {
                "code": l.get('adminCode3'),
                "name": l.get('adminName3')
            },
            "admin4": {
                "code": l.get('adminCode4'),
                "name": l.get('adminName4')
            }
        })
    return locs


def get_activity_dict(id, locations_dict):
    return {
        "project_id": id,
        "locations": locations_dict
    }

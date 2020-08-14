import datetime
import json
import logging.config
import os
import threading
import uuid

from flask import Flask, render_template
from flask import Response
from flask import request
from flask_cors import CORS

from banner import print_banner
from dg.geocoder.amp.amp_location_matcher import get_matched_amp_locations
from dg.geocoder.config import get_web_log_config_path, get_doc_queue_path, get_default_country
from dg.geocoder.db.amp_location import clean_amp_locations, save_amp_locations, get_amp_locations
from dg.geocoder.db.doc_queue import add_activity_job_to_queue, get_queue_by_id_with_extract_info
from dg.geocoder.db.geocode import save_activity, get_geocode_by_id
from dg.geocoder.util.file_util import JSON
from scheduler import process_all_pending_jobs

logging.config.fileConfig(get_web_log_config_path())
logger = logging.getLogger()

print_banner()

app = Flask(__name__)

CORS(app)


@app.route('/')
def upload():
    return render_template("file_upload_form.html")


@app.route('/success', methods=['POST'])
def success():
    if request.method == 'POST':
        f = request.files['file']
        f.save(f.filename)
        return render_template("success.html", name=f.filename)


def datetime_handler(x):
    if isinstance(x, datetime.datetime):
        return x.isoformat()
    raise TypeError("Unknown type")


@app.route('/')
def root():
    return app.send_static_file('index.html')


@app.route('/activity/process', methods=['POST'])
def geocode():
    """
    upload list of amp activities
    """
    country_code = get_default_country()
    file_type = JSON
    amp_queue_relations = []
    for activity in request.json:
        file_name = str(uuid.uuid4()) + '.json'
        docs_path = os.path.join(get_doc_queue_path(), file_name)
        f = open(docs_path, "w")
        f.write(json.dumps(activity))
        f.close()
        identifier = save_activity(activity['amp_id'])
        queue_id = add_activity_job_to_queue(file_name, file_type, country_code, identifier)
        amp_queue_relations.append(dict(amp_id=activity['amp_id'], queue_id=queue_id))

    th = threading.Thread(target=process_all_pending_jobs)
    th.start()

    return Response(json.dumps(amp_queue_relations), mimetype='application/json'), 201


@app.route('/geocode', methods=['GET'])
def geocoding_list():
    geocode_id = None
    if 'id' in request.args:
        geocode_id = request.args['id']
    else:
        return Response(json.dumps(dict(error="No id field provided. Please specify an id."),
                                   default=datetime_handler), mimetype='application/json'), 400

    return Response(json.dumps(get_geocode_by_id(geocode_id), default=datetime_handler), mimetype='application/json')


@app.route('/queue', methods=['GET'])
def get_queue_by_id():
    queue_id = None
    if 'id' in request.args:
        queue_id = request.args['id']
    else:
        return Response(json.dumps(dict(error="No id field provided. Please specify an id."),
                                   default=datetime_handler), mimetype='application/json'), 400

    data = get_queue_by_id_with_extract_info(queue_id=queue_id)
    if data is None or len(data) == 0:
        return Response(json.dumps(dict(error="No queue find with the specified id."),
                        default=datetime_handler), mimetype='application/json'), 404

    results = dict(id=data[0]['id'], state=data[0]['state'], message=data[0]['message'], amp_id=data[0]['amp_id'],
                   extract_data=[])

    amp_locations = get_amp_locations()
    for e in data:
        matched_amp_locations = get_matched_amp_locations([get_geocode_by_id(e['geocoding_id'])], amp_locations)
        matched_amp_location_ids = None
        if matched_amp_locations is not None:
            matched_amp_location_ids = [loc['amp_location_id'] for loc in matched_amp_locations]

        results['extract_data'].append(
            dict(field_name=e['field_name'], entities=e['entities'], text=e['text'], geocoding_id=e['geocoding_id'],
                 amp_location_id=matched_amp_location_ids))

    return Response(json.dumps(results, default=datetime_handler), mimetype='application/json')


@app.route('/amp/locations', methods=['PUT'])
def create_amp_locations():
    save_amp_locations(request.json)

    return "OK", 200


@app.route('/amp/locations', methods=['GET'])
def get_all_amp_locations():
    amp_locations = get_amp_locations()

    return Response(json.dumps(amp_locations, default=datetime_handler), mimetype='application/json')


@app.route('/amp/locations', methods=['DELETE'])
def delete_amp_locations():
    clean_amp_locations()

    return "OK", 200


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)

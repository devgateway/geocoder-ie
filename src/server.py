import datetime
import json
import logging.config
import os
import threading
import eventlet

from os.path import sep
from urllib.parse import unquote

import time
from flask import Flask, jsonify
from flask import Response
from flask import request
from flask.helpers import send_from_directory, stream_with_context
from flask_cors import CORS

from banner import print_banner
from dg.geocoder.config import get_doc_queue_path, get_app_port, get_log_config_path, get_web_log_config_path
from dg.geocoder.constants import ST_PROCESSING, ST_PENDING, ST_PROCESSED, ST_ERROR
from dg.geocoder.db.corpora import get_sentences, delete_sentence, set_category, get_sentence_by_id, get_doc_list
from dg.geocoder.db.doc_queue import add_job_to_queue, get_queue_list, get_queue_by_id, delete_doc_from_queue, \
    delete_all_docs_from_queue
from dg.geocoder.db.geocode import get_geocoding_list, get_extracted_list, get_activity_list
from shelljob import proc

logging.config.fileConfig(get_web_log_config_path())
logger = logging.getLogger()

print_banner()

app = Flask(__name__, static_url_path="", static_folder="../static")

CORS(app)


def datetime_handler(x):
    if isinstance(x, datetime.datetime):
        return x.isoformat()
    raise TypeError("Unknown type")


@app.route('/')
def root():
    return app.send_static_file('index.html')


@app.route('/download/<doc_id>', methods=['GET'])
def doc_download(doc_id):
    sentence = get_sentence_by_id(doc_id)
    path = sentence[3]
    full_path = os.path.realpath(os.path.realpath(os.path.join('', path)))
    parts = full_path.split(os.path.sep)

    return send_from_directory(sep.join(parts[0:-1]), parts[-1], as_attachment=True)


@app.route('/corpora', methods=['GET'])
def corpora_list():
    page = 1
    query = None
    category = None
    doc = None
    if 'page' in request.args:
        page = request.args['page']

    if 'query' in request.args:
        query = request.args['query']

    if 'category' in request.args:
        category = request.args['category']

    if 'doc' in request.args:
        doc = unquote(request.args['doc'])

    return Response(json.dumps(get_sentences(page=page, query=query, category=category, document=doc)),
                    mimetype='application/json')


@app.route('/corpora/docs', methods=['GET'])
def corpora_docs_list():
    return Response(json.dumps(get_doc_list()), mimetype='application/json')


@app.route('/corpora/<corpora_id>', methods=['DELETE'])
def corpora_delete(corpora_id):
    if delete_sentence(corpora_id):
        return jsonify({"success": True}), 200
    else:
        return jsonify({"success": False}), 500


@app.route('/corpora/<corpora_id>', methods=['POST'])
def corpora_set_category(corpora_id):
    if set_category(corpora_id, request.json['category']):
        return jsonify({"success": True}), 200
    else:
        return jsonify({"success": False}), 500


@app.route('/docqueue', methods=['GET'])
def docs_list():
    page = 1
    doc_type = None
    state = None
    if 'page' in request.args:
        page = request.args['page']

    if 'doc_type' in request.args:
        doc_type = request.args['doc_type']

    if 'state' in request.args:
        state = request.args['state']
        states = [state]
        if state == ST_PENDING:
            states.append(ST_PROCESSING)

        if state == ST_PROCESSED:
            states.append(ST_ERROR)

    return Response(json.dumps(get_queue_list(page=page, doc_type=doc_type, states=states), default=datetime_handler),
                    mimetype='application/json')


@app.route('/docqueue/download/<file>', methods=['GET'])
def file_download(file):
    return send_from_directory(get_doc_queue_path(), file, as_attachment=True)


@app.route('/docqueue/<document_id>', methods=['DELETE'])
def docqueue_delete(document_id):
    threads = [t for t in threading.enumerate() if t.name == document_id]
    if len(threads) > 0:
        logger.warning('Warning thread still alive')
        return jsonify({"success": False}), 200
    else:
        if delete_doc_from_queue(document_id):
            return jsonify({"success": True}), 200
        else:
            return jsonify({"success": False}), 500


@app.route('/docqueue/upload', methods=['GET', 'POST'])
def upload_doc():
    if request.method == 'POST':
        f = request.files['file']
        country_code = request.form['countryISO']
        file_name = f.filename
        file_type = f.content_type
        docs_path = os.path.join(get_doc_queue_path(), file_name)
        f.save(docs_path)
        add_job_to_queue(file_name, file_type, country_code)
    return jsonify({"success": True}), 200


@app.route('/docqueue/process/<document_id>', methods=['GET'])
def process_document(document_id):
    logger.info('starting process thread')
    # a_thread = threading.Thread(name=document_id, target=process_by_id, args=(document_id,))
    # a_thread.start()
    # return jsonify({"success": True}), 200


@app.route('/geocoding', methods=['GET'])
def geocoding_list():
    activity_id = None
    queue_id = None
    if 'activity_id' in request.args:
        activity_id = request.args['activity_id']

    if 'queue_id' in request.args:
        queue_id = request.args['queue_id']

    return Response(json.dumps(get_geocoding_list(activity_id=activity_id, queue_id=queue_id),
                               default=datetime_handler), mimetype='application/json')


@app.route('/geocoding/download/<queue_id>', methods=['GET'])
def geocoding_download(queue_id):
    queue = get_queue_by_id(queue_id)
    if queue.get('queue_type') != 'ACTIVITY_QUEUE':
        doc_name = queue.get('out_file')
        return send_from_directory(get_doc_queue_path(), doc_name, as_attachment=True)


@app.route('/activity', methods=['GET'])
def activity_list():
    document_id = None
    if 'document_id' in request.args:
        document_id = request.args['document_id']

    return Response(json.dumps(get_activity_list(document_id=document_id),
                               default=datetime_handler), mimetype='application/json')


@app.route('/extracted', methods=['GET'])
def extracted_list():
    geocoding_id = None
    if 'geocoding_id' in request.args:
        geocoding_id = request.args['geocoding_id']

    return Response(json.dumps(get_extracted_list(geocoding_id=geocoding_id),
                               default=datetime_handler), mimetype='application/json')


@app.route('/docqueue/purge', methods=['GET'])
def purge():
    delete_all_docs_from_queue()
    return jsonify({"insane": True}), 200


@app.route('/stream')
def stream():
    g = proc.Group()
    g.run(["bash", "-c", "tail -f /var/log/geocoder.log"])

    def read_process():
        trigger_time = time.time() + 5
        while g.is_pending():
            lines = g.readlines()
            for proc, line in lines:
                yield line

            now = time.time()
            if now > trigger_time:
                yield "*** Interval"
                trigger_time = now + 5

    return Response(stream_with_context(read_process()))


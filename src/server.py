import datetime
import json
import logging
import os
import threading
from os.path import sep
from urllib.parse import unquote

from flask import Flask, jsonify
from flask import Response
from flask import request
from flask.helpers import send_from_directory
from flask_cors import CORS

from dg.geocoder.config import get_doc_queue_path, get_app_port
from dg.geocoder.db.corpora import get_sentences, delete_sentence, set_category, get_sentence_by_id, get_doc_list
from dg.geocoder.db.doc_queue import save_doc, get_docs, get_document_by_id, delete_doc_from_queue
from dg.geocoder.db.geocode import get_geocoding_list, get_extracted_list, get_activity_list
from dg.geocoder.processor import process_by_id

logger = logging.getLogger()

app = Flask(__name__, static_url_path="", static_folder="../static")

CORS(app)


def datetime_handler(x):
    if isinstance(x, datetime.datetime):
        return x.isoformat()
    raise TypeError("Unknown type")


@app.route('/')
def root():
    return app.send_static_file('index.html')


@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        f = request.files['the_file']
        f.save('/var/www/uploads/uploaded_file.txt')


@app.route('/download/<id>', methods=['GET'])
def doc_download(id):
    sentence = get_sentence_by_id(id)
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


@app.route('/corpora/<id>', methods=['DELETE'])
def corpora_delete(id):
    if delete_sentence(id):
        return jsonify({"success": True}), 200
    else:
        return jsonify({"success": False}), 500


@app.route('/corpora/<id>', methods=['POST'])
def corpora_set_category(id):
    if set_category(id, request.json['category']):
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

    return Response(json.dumps(get_docs(page=page, doc_type=doc_type, state=state), default=datetime_handler),
                    mimetype='application/json')


@app.route('/docqueue/<id>', methods=['DELETE'])
def docqueue_delete(id):
    if delete_doc_from_queue(id):
        return jsonify({"success": True}), 200
    else:
        return jsonify({"success": False}), 500


@app.route('/docqueue/upload', methods=['GET', 'POST'])
def upload_doc():
    if request.method == 'POST':
        f = request.files['file']
        countryISO = request.form['countryISO']
        filename = f.filename
        filetype = f.content_type
        docs_path = os.path.join(get_doc_queue_path(), filename)
        f.save(docs_path)
        save_doc(filename, filetype, countryISO)
    return jsonify({"success": True}), 200


@app.route('/docqueue/process/<id>', methods=['GET'])
def process_document(id):
    logger.info('starting process thread')
    a_thread = threading.Thread(target=process_by_id, args=(id,))
    a_thread.start()
    return jsonify({"success": True}), 200


@app.route('/geocoding', methods=['GET'])
def geocoding_list():
    activity_id = None
    document_id = None
    if 'activity_id' in request.args:
        activity_id = request.args['activity_id']

    if 'document_id' in request.args:
        document_id = request.args['document_id']

    return Response(json.dumps(get_geocoding_list(activity_id=activity_id, document_id=document_id),
                               default=datetime_handler), mimetype='application/json')


@app.route('/geocoding/download/<id>', methods=['GET'])
def geocoding_download(id):
    document = get_document_by_id(id)
    doc_name = document[1]
    doc_type = document[2]
    output_ext = '_out.tsv'
    if doc_type == 'text/xml':
        output_ext = '_out.xml'
    return send_from_directory(get_doc_queue_path(), doc_name.split('.')[0] + output_ext, as_attachment=True)


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


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=get_app_port(), debug=True)

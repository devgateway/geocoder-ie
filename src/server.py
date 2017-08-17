import json
import os
from os.path import sep
from urllib.parse import unquote

from flask import Flask, jsonify
from flask import Response
from flask import request
from flask.helpers import send_from_directory
from flask_cors import CORS
from dg.geocoder.config import get_doc_queue_path, get_app_port
from dg.geocoder.db.corpora import get_sentences, delete_sentence, set_category, get_sentence_by_id, get_doc_list
from dg.geocoder.db.doc_queue import save_doc, get_docs
import datetime

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


@app.route('/docqueue/upload', methods=['GET', 'POST'])
def upload_doc():
    if request.method == 'POST':
        f = request.files['file']
        countryISO = request.form['countryISO']
        filename = f.filename
        filetype = f.content_type
        docs_path = get_doc_queue_path()+"""\\"""+filename
        f.save(docs_path)
        save_doc(filename, filetype, countryISO)
    return jsonify({"success": True}), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=get_app_port(), debug=True)

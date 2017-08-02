import json
import os
from os.path import sep
from urllib.parse import unquote

from flask import Flask, jsonify
from flask import Response
from flask import request
from flask.helpers import send_from_directory
from flask_cors import CORS

from dg.geocoder.db.corpora import get_sentences, delete_sentence, set_category, get_sentence_by_id, get_doc_list

app = Flask(__name__, static_url_path="", static_folder="../static")

CORS(app)


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


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)

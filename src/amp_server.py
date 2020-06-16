import datetime
import logging.config

from flask import Flask, jsonify, render_template
from flask import request
from flask_cors import CORS

from banner import print_banner
from dg.geocoder.config import get_web_log_config_path

logging.config.fileConfig(get_web_log_config_path())
logger = logging.getLogger()

print_banner()

app = Flask(__name__)

CORS(app)


@app.route('/')
def upload():
    return render_template("file_upload_form.html")


@app.route('/success', methods = ['POST'])
def success():
    if request.method == 'POST':
        f = request.files['file']
        f.save(f.filename)
        return render_template("success.html", name = f.filename)


def datetime_handler(x):
    if isinstance(x, datetime.datetime):
        return x.isoformat()
    raise TypeError("Unknown type")


@app.route('/')
def root():
    return app.send_static_file('index.html')


@app.route('/upload', methods=['POST'])
def geocode():
    if request.method == 'POST':
        json = request.json
        for activity in json:
            print(activity['amp_id'])
    return jsonify({"success": True}), 200


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)

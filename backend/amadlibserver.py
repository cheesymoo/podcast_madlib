import os
import yaml
import logging
import logging.config
import random

from flask import Flask, send_from_directory, abort, Response, request, jsonify

app = Flask(__name__)
application = app

CONFIG_FILE = os.path.join(os.path.dirname(__file__), "audiomadlib.cfg")

MADLIBS_DIR = os.path.join(os.path.dirname(__file__), "madlibs")

logging.config.fileConfig(CONFIG_FILE)

logger = logging.getLogger("http_server")


@app.route("/backend/list_madlibs")
def list_madlibs():
    madlibs = []
    for filename in os.listdir(MADLIBS_DIR):
        if not filename.endswith(".yaml"):
            continue
        full_filename = os.path.join(MADLIBS_DIR, filename)
        madlib = yaml.load(open(full_filename))
        madlib["key"] = filename[:-5]
        madlibs.append(madlib)
    random.shuffle(madlibs)
    resp = jsonify(madlibs)
    h = resp.headers 
    h["Access-Control-Allow-Origin"] = "*"
    h["Access-Control-Allow-Headers"] = "Origin, X-Requested-With, Content-Type, Accept"
    h["Access-Control-Allow-Methods"] = "GET, OPTIONS"
    return resp


# For debug
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    return 'You want path: %s' % path

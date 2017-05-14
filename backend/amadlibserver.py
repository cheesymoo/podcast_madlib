import os
import yaml
import logging
import logging.config
import random

from flask import Flask, send_from_directory, abort, Response, request, jsonify

from amadlib import read_madlibs

app = Flask(__name__)
application = app

CONFIG_FILE = os.path.join(os.path.dirname(__file__), "audiomadlib.cfg")

logging.config.fileConfig(CONFIG_FILE)

logger = logging.getLogger("http_server")


@app.route("/backend/list_madlibs")
def list_madlibs():
    madlibs = read_madlibs()
    logger.info("list_madlibs: %d madlibs", len(madlibs))
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
    logger.info("catch_all for path: %s, request.args: %s, request.form: %s, request.files: %s",
                path, request.args, request.form, request.files)
    return 'You want path: %s' % path

import uuid
import os
import yaml
import logging
import logging.config
import random

from flask import Flask, send_from_directory, abort, Response, request, jsonify

from amadlib import read_madlibs, generate_output

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

@app.route('/backend/send_recording/<key>/', methods=["POST", 'OPTIONS', "GET"])
def send_recording(key):
    logger.info("send_recording %s", key)
    task_id = str(uuid.uuid4())
    logger.debug("task_id(%s)", task_id)
    audio_file = request.files["data"]
    wav_filename = "user_input/%s.wav" % task_id
    open(wav_filename, "wb").write(audio_file.read())
    generate_output(key, wav_filename, task_id)
    resp = jsonify({"output": task_id + ".mp3"})
    h = resp.headers
    h["Access-Control-Allow-Origin"] = "*"
    h["Access-Control-Allow-Headers"] = "Origin, X-Requested-With, Content-Type, Accept"
    h["Access-Control-Allow-Methods"] = "GET, OPTIONS"
    return resp


# For debug
@app.route('/', defaults={'path': ''}, methods=['GET', "POST", 'OPTIONS'])
@app.route('/<path:path>', methods=['GET', "POST", 'OPTIONS'])
def catch_all(path):
    logger.info("catch_all for path: %s, request.args: %s, request.form: %s, request.files: %s",
                path, request.args, request.form, request.files)
    resp = jsonify({"catch_all": path})
    h = resp.headers
    h["Access-Control-Allow-Origin"] = "*"
    h["Access-Control-Allow-Headers"] = "Origin, X-Requested-With, Content-Type, Accept"
    h["Access-Control-Allow-Methods"] = "GET, OPTIONS"
    return resp

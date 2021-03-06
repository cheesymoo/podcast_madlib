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
    resp = jsonify({"output": task_id + ".mp3",
	"url": "https://pdcmadlib.radiocut.fm/backend/listen/%s/%s/" % (key, task_id)
    })
    h = resp.headers
    h["Access-Control-Allow-Origin"] = "*"
    h["Access-Control-Allow-Headers"] = "Origin, X-Requested-With, Content-Type, Accept"
    h["Access-Control-Allow-Methods"] = "GET, OPTIONS"
    return resp

@app.route('/backend/listen/<key>/<uuid>/', methods=["GET"])
def listen(key, uuid):
    madlibs = read_madlibs()
    madlib = [m for m in madlibs if m["key"] == key][0]
    template_filename = os.path.join(os.path.dirname(__file__), "../src/template.html")
    template = open(template_filename).read()
    image = "https://pdcmadlib.radiocut.fm/be-images/%s" % madlib["interviewer_photo"] if madlib["interviewer_photo"] else "https://placehold.it/350x150"
    output = template.format(url="https://pdcmadlib.radiocut.fm/backend/listen/%s/%s/" % (key, uuid),
                             image=image,
                             link=madlib["link"],
                             outputfile="https://pdcmadlib.radiocut.fm/output/%s.mp3" % uuid,
                             )
    return output

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

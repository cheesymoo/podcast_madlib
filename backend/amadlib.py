import os
import yaml
import subprocess
import logging

logger = logging.getLogger()

MADLIBS_DIR = os.path.join(os.path.dirname(__file__), "madlibs")

def read_madlibs():
    madlibs = []
    for filename in os.listdir(MADLIBS_DIR):
        if not filename.endswith(".yaml"):
            continue
        full_filename = os.path.join(MADLIBS_DIR, filename)
        madlib = yaml.load(open(full_filename))
        madlib["key"] = filename[:-5]
        madlibs.append(madlib)
    return madlibs

def generate_output(key, input_filename, uuid):
    logger.debug("generate_output(%s, %s)", key, uuid)
    madlib = [m for m in read_madlibs() if m["key"] == key][0]
    question = "media/" + madlib["parts"][0]["file"]
    answer = "user_input/%s.mp3" % uuid
    output = "output/%s.mp3" % uuid
    logger.debug("filenames %s %s %s", question, input_filename, answer)

    if input_filename != answer:
        # Conversion
        ffmpeg_call = ["/usr/bin/ffmpeg", "-n", "-i", input_filename, "-ar", "48000", answer]
        logger.info("ffmpeg call: %s", " ".join(ffmpeg_call))
        try:
            retcode = subprocess.call(ffmpeg_call)
        except:
            logger.exception("error calling %s", ffmpeg_call)
        logger.info("retcode %s", retcode)

    ffmpeg_call = ["/usr/bin/ffmpeg", "-n",
                   "-loglevel", "warning",
                   "-i", "concat:" + "%s|%s" % (question, answer),
                   "-acodec", "copy",
                   output]
    logger.info("ffmpeg call: %s", " ".join(ffmpeg_call))
    retcode = subprocess.call(ffmpeg_call)
    logger.info("retcode %s", retcode)
    return retcode, output

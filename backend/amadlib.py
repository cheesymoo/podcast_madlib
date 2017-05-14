import os
import yaml


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

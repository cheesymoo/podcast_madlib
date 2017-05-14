import os
import csv
import sys

rows = list(csv.reader(open("Questions.csv")))[1:]

for i, row in enumerate(rows):
    text = open("madlibs/madlib.yaml.template").read()
    filename = row[0].strip()
    if not os.path.exists("media/%s.mp3" % filename):
        print("Error line %d: %s does not exists!" % (i + 1, filename))
        continue
    new_yaml = text.format(question=row[2], interviewer=row[1], filename=filename)
    open("madlibs/q%d.yaml" % i, "wt").write(new_yaml)

import os
import csv
import sys

rows = list(csv.reader(open("Questions.csv")))[1:]

for i, row in enumerate(rows):
    text = open("madlibs/madlib.yaml.template").read()
    if not os.path.exists("media/%s.mp3" % row[0]):
        print("Error line %d: %s does not exists!" % (i + 1, row[0]))
        continue
    new_yaml = text.format(question=row[2], interviewer=row[1], filename=row[0])
    open("madlibs/q%d.yaml" % i, "wt").write(new_yaml)

import os
import csv
import sys

rows = list(csv.reader(open("Questions.csv")))[1:]

for i, row in enumerate(rows):
    text = open("madlibs/madlib.yaml.template").read()
    filename = row[0].strip()
    interviewer = row[1].strip()
    if not os.path.exists("media/%s.mp3" % filename):
        print("Error line %d: %s does not exists!" % (i + 1, filename))
        continue
    interviewer_img = interviewer.replace(" ", "_") + ".jpg"
    if not os.path.exists("images/%s.jpg" % interviewer.replace(" ", "_")):
        print("Error line %d: %s interviewer image does not exists!" % (i + 1, interviewer))
        interviewer_img = ""
    link = row[3].strip() if len(row) > 3 else ""
    new_yaml = text.format(question=row[2], interviewer=row[1], filename=filename, 
	interviewer_img=interviewer_img, link=link)
    open("madlibs/q%d.yaml" % i, "wt").write(new_yaml)

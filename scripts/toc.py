#!/usr/bin/python
# -*- coding: utf-8 -*-
# Usage: ./toc.py < toc.csv > toc.txt
# Takes Tan Cunda's ToC CSV and makes appropriate filenames (sans extension)
# in the appropriate order
import sys
import csv
import re
import utils

infile = sys.stdin
outfile = sys.stdout

reader = csv.reader(infile)

for row in reader:
    author = row[0].strip().lower()
    date = row[3].strip()
    title = row[4].strip()
    cleantitle = utils.mangle_title(title.decode("utf-8"))
    cleantitle = cleantitle.encode("utf-8")

    title = title.lower().decode("utf-8")
    title = re.sub(ur"[^a-zāīūṃṅñṭḍṇḷ ]", "", title)
    title = re.sub(r"\s+", "-", title)
    outfile.write("%s-%s-%s\n" % (author, date, cleantitle))

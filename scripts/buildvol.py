#!/usr/bin/python
# -*- coding: utf-8 -*-
# Usage ./buildvol.py < volN-toc.csv > volN.md
# Takes a table of contents file in csv (author, date, title) and
# outputs a markdown file with contents of the talks in the of the rows
# in the TOC file.
import sys
import re
import csv
from cStringIO import StringIO

authorfiles = {
    u"Luang Por Pasanno": "lpp.md",
    u"Ajahn Amaro": "aa.md",
    u"Ajahn Yatiko": "ay.md",
    u"Ajahn Karuṇadhammo": "akd.md",
    u"Ajahn Jotipālo": "ajo.md",
    u"Ajahn Ñāṇiko": "an.md",
    u"Ajahn Vīradhammo": "av.md",
    u"Ajahn Sucitto": "asuc.md",
}

talks = {
    u"Luang Por Pasanno": {},
    u"Ajahn Amaro": {},
    u"Ajahn Yatiko": {},
    u"Ajahn Karuṇadhammo": {},
    u"Ajahn Jotipālo": {},
    u"Ajahn Ñāṇiko": {},
    u"Ajahn Vīradhammo": {},
    u"Ajahn Sucitto": {},
}

buf = StringIO()

for author in authorfiles:
    title = None
    date = None
    afile = open(authorfiles[author])
    line = afile.readline()
    while line:
        m = re.match(r"(#+) (.*)\n", line)
        if m:
            prefix = m.group(1)
            text = m.group(2).decode("utf-8")

            if prefix == "#":
                content = buf.getvalue()
                if content:
                    talks[author][title] = content
                buf.truncate(0)
                title = text
            elif prefix == "###":
                date = text
                talks[author][title] = date
        buf.write(line)
        line = afile.readline()


infile = sys.stdin
outfile = sys.stdout

reader = csv.reader(infile)

for row in reader:
    author = row[0].decode("utf-8")
    #date = row[1]
    title = row[2].decode("utf-8")
    outfile.write(talks[author][title])

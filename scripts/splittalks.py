#!/usr/bin/python
# -*- coding: utf-8 -*-
# Usage: ./splittalks.py < all.md
# splits a composite markdown file into invidiual talks
# named ./author-date-title.md, all lower case, spaces -> hyphens
import sys
import re
from cStringIO import StringIO
import utils

infile = sys.stdin
#outfile = sys.stdout
buf = StringIO()

line = infile.readline()

authors = {
    "Luang Por Pasanno": "lpp",
    "Ajahn Amaro": "aa",
    "Ajahn Yatiko": "ay",
    u"Ajahn Karuṇadhammo": "akd",
    u"Ajahn Jotipālo": "ajo",
    u"Ajahn Ñāṇiko": "an",
    "Ajahn Vīradhammo": "av",
    "Ajahn Sucitto": "asuc",
}

while line:
    m = re.match("# (.*)", line)
    if m:
        if buf.getvalue():
            if author in authors:
                shortauthor = authors[author]
            else:
                shortauthor = author
            cleantitle = utils.mangle_title(title.decode("utf-8"))
            cleantitle = cleantitle.encode("utf-8")
            outfile = open("%s-%s-%s.md" % (shortauthor, date, cleantitle), "w")
            outfile.write("# %s\n" % title)
            outfile.write("## %s\n" % author)
            outfile.write("### %s\n" % date)
            buf.seek(0)
            outfile.write(buf.read())
            outfile.close()
            buf.truncate(0)
        title = m.group(1).strip()
    else:
        m = re.match("## (.*)", line)
        if m:
            author = m.group(1).strip()
        else:
            m = re.match("### (.*)", line)
            if m:
                date = m.group(1).strip()
            else:
                buf.write(line)
    line = infile.readline()

if buf.getvalue():
    if author in authors:
        shortauthor = authors[author]
    else:
        shortauthor = author
    cleantitle = utils.mangle_title(title.decode("utf-8"))
    cleantitle = cleantitle.encode("utf-8")
    outfile = open("%s-%s-%s.md" % (shortauthor, date, cleantitle), "w")
    outfile.write("# %s\n" % title)
    outfile.write("## %s\n" % author)
    outfile.write("### %s\n" % date)
    buf.seek(0)
    outfile.write(buf.read())
    outfile.close()

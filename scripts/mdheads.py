#!/usr/bin/python
# -*- coding: utf-8 -*-
# Usage ./md-heads < in.md > out.md
# Takes vanilla markdown from LibreOffice html | `pandoc -t markdown` and
# arranges the title/author/date sequence while adding ATX-sytle headers
import sys

authors = (
    "Luang Por Pasanno\n",
    "Ajahn Amaro\n",
    "Ajahn Yatiko\n",
    "Ajahn Karuṇadhammo\n",
    "Ajahn Jotipālo\n",
    "Ajahn Ñāṇiko\n",
    "Ajahn Vīradhammo\n",
    "Ajahn Sucitto\n",
)

infile = sys.stdin
outfile = sys.stdout

line = infile.readline()

while line:
    if line in authors:
        author = line
        infile.readline() # blank
        date = infile.readline()
        infile.readline() # blank
        title = infile.readline()
        outfile.write("# " + title + "\n")
        outfile.write("## " + author + "\n")
        outfile.write("### " + date)
    else:
        outfile.write(line)
    line = infile.readline()

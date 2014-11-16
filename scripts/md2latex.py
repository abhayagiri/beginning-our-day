#!/usr/bin/python
# -*- encoding: utf-8 -*-
# Usage: html2latex.py < INFILE.html > OUTFILE.tex
import sys
from cStringIO import StringIO
import os
import re
import subprocess
from lxml import etree
from lxml import sax
import xml.sax.handler

authors = {
    u"Luang Por Pasanno": "lpp",
    u"Ajahn Amaro": "aa",
    u"Ajahn Yatiko": "ay",
    u"Ajahn Karuṇadhammo": "akd",
    u"Ajahn Jotipālo": "ajo",
    u"Ajahn Ñāṇiko": "an",
    u"Ajahn Vīradhammo": "av",
    u"Ajahn Sucitto": "asuc",
}

months = {
    "01": "January",
    "02": "February",
    "03": "March",
    "04": "April",
    "05": "May",
    "06": "June",
    "07": "July",
    "08": "August",
    "09": "September",
    "10": "October",
    "11": "November",
    "12": "December",
}


class Html2Latex(xml.sax.handler.ContentHandler):
    def __init__(self, outfile=sys.stdout):
        xml.sax.handler.ContentHandler.__init__(self)
        self.outfile = outfile
        self.path = []
        self.curtitle = None
        self.curauthor = None
        self.curdate = None
    def characters(self, content):
        content = re.sub('\n', ' ', content)
        if content:
            content = re.sub(r'\.\.\.', r'\ldots{}', content)
            content = re.sub(ur'\u201c', '``', content)
            content = re.sub(ur'\u201d', '\'\'', content)
            content = re.sub(ur'\u2018', '`', content)
            content = re.sub(ur'\u2019', '\'', content)
            content = re.sub(ur'\u2014', '---', content)
            cur = self.path[-1]
            if cur == 'h1':
                self.curtitle = content.encode('utf-8')
            elif cur == 'h2':
                m = re.match(ur'(.*) • (.*)', content)
                if m is None:
                    print "WHOOPS"
                    print content.encode('utf-8')
                    sys.exit(1)
                self.curauthor = m.group(1).encode('utf-8')
                self.curdate = m.group(2).encode('utf-8')
            #elif cur == 'h3':
            #    m = re.match(r'(..)-(..)-(..)', content)
            #    self.curdate = '%s 20%s' % (months[m.group(1)], m.group(3))
            else:
                self.outfile.write(content.encode('utf-8'))
    def startElementNS(self, name, qname, attrs):
        self.path.append(qname)
        if qname == 'p':
            pass
        elif qname == 'em':
            self.outfile.write(r'\emph{')
        elif qname == 'h1':
            pass
        elif qname == 'blockquote':
            self.outfile.write('\\begin{quote}\n')
    def endElementNS(self, name, qname):
        self.path.pop()
        if qname == 'p':
            self.outfile.write('\n\n')
        elif qname == 'em':
            self.outfile.write('}')
        elif qname == 'blockquote':
            self.outfile.write('\\end{quote}\n\n')
        elif qname == 'br':
            self.outfile.write('\\\\\n')
        elif qname == 'h2':
            self.outfile.write('\\mychapter{%s}{%s}{%s}\n\n'
                % (self.curtitle, self.curauthor, self.curdate))

infile = sys.stdin
outfile = sys.stdout



pandoc = subprocess.Popen(['pandoc', '-f', 'markdown', '-t', 'html', '-S'],
    stdin=infile, stdout=subprocess.PIPE)
sed = subprocess.Popen(['sed', 's/^[[:space:]]*//'],
    stdin=subprocess.PIPE, stdout=subprocess.PIPE)
fold = subprocess.Popen(['fold', '-s', '-w', '72'],
    stdin=sed.stdout, stdout=outfile)
#pandoc.stdin.write(infile.read())
#pandoc.stdin.close()
tree = etree.parse(pandoc.stdout, etree.HTMLParser(encoding='utf-8'))
sax.saxify(tree, Html2Latex(sed.stdin))
sed.stdin.close()

#outfile.write(fold.stdout.read())

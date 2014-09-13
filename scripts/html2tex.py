#!/usr/bin/python
import sys
import re
from lxml import etree
from lxml import sax
import xml.sax.handler

infile = sys.stdin
outfile = sys.stdout

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


class Handler(xml.sax.handler.ContentHandler):
    def __init__(self, outfile=sys.stdout):
        xml.sax.handler.ContentHandler.__init__(self)
        self.outfile = outfile
        self.path = []
        self.curtitle = None
        self.curauthor = None
        self.curdate = None
    def characters(self, content):
        content = content.strip('\n')
        if content:
            content = re.sub(r'\.\.\.', r'\ldots{}', content)
            content = re.sub(ur'\u201c', '``', content)
            content = re.sub(ur'\u201d', '\'\'', content)
            content = re.sub(ur'\u2018', '`', content)
            content = re.sub(ur'\u2019', '\'', content)
            content = re.sub(ur'\u2014', '---', content)
            content = content.encode('utf-8')
            cur = self.path[-1]
            if cur == 'h1':
                self.curtitle = content
            elif cur == 'h2':
                self.curauthor = content
            elif cur == 'h3':
                m = re.match(r'(..)-(..)-(..)', content)
                self.curdate = '%s 20%s' % (months[m.group(1)], m.group(3))
            else:
                self.outfile.write(content)
    def startElementNS(self, name, qname, attrs):
        self.path.append(qname)
        if qname == 'p':
            pass
        elif qname == 'em':
            self.outfile.write(r'\emph{')
        elif qname == 'h1':
            pass
    def endElementNS(self, name, qname):
        self.path.pop()
        if qname == 'p':
            self.outfile.write('\n\n')
        elif qname == 'em':
            self.outfile.write('}')
        elif qname == 'h3':
            self.outfile.write('\\mychapter{%s}{%s}{%s}\n\n'
                % (self.curtitle, self.curauthor, self.curdate))

tree = etree.parse(infile, etree.HTMLParser(encoding='utf-8'))
sax.saxify(tree, Handler())

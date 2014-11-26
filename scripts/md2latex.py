#!/usr/bin/python
# -*- encoding: utf-8 -*-
# Usage: html2latex.py < INFILE.html > OUTFILE.tex
import sys
import os
import re
import subprocess
from lxml import etree
from lxml import sax
import xml.sax.handler
from encodings import utf_8

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
            content = re.sub(r'\. \. \.', r'\ldots{}', content)
            content = re.sub(ur'\u2026', r'\ldots{}', content)
            content = re.sub(ur'\u201c', '``', content)
            content = re.sub(ur'\u2019\u201d', r"'\\thinspace''", content)
            content = re.sub(ur'\u201d', '\'\'', content)
            content = re.sub(ur'\u2018', '`', content)
            content = re.sub(ur'\u2019', '\'', content)
            content = re.sub(ur'\u2014', '---', content)
            cur = self.path[-1]
            if cur == 'h1':
                self.curtitle = content
            elif cur == 'h2':
                m = re.match(ur'(.*) • (.*)', content)
                if m is None:
                    print "WHOOPS"
                    print content
                    sys.exit(1)
                self.curauthor = m.group(1)
                self.curdate = m.group(2)
            #elif cur == 'h3':
            #    m = re.match(r'(..)-(..)-(..)', content)
            #    self.curdate = '%s 20%s' % (months[m.group(1)], m.group(3))
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


pandoc = subprocess.Popen(['pandoc', '-f', 'markdown', '-t', 'html'],
    stdin=infile, stdout=subprocess.PIPE)
sed = subprocess.Popen(['sed', 's/^[[:space:]]*//'],
    stdin=subprocess.PIPE, stdout=subprocess.PIPE)
coder = utf_8.StreamWriter(sed.stdin)
fold = subprocess.Popen(['fold', '-s', '-w', '72'],
    stdin=sed.stdout, stdout=outfile)
#pandoc.stdin.write(infile.read())
#pandoc.stdin.close()
tree = etree.parse(pandoc.stdout, etree.HTMLParser(encoding='utf-8'))
sax.saxify(tree, Html2Latex(coder))
sed.stdin.close()

#outfile.write(fold.stdout.read())

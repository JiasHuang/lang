#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import os
import random

from optparse import OptionParser

import page
import meta

def loadWord(req, url):
    return parseWord(req, meta.load(url))

def parseWord(req, txt):
    dictYahoo = 'https://tw.dictionary.yahoo.com/dictionary?p='
    txt = re.sub('strong>', 'b>', txt)
    for m in re.finditer(r'<b>([^<]*)</b>', txt):
        q = m.group(1).rstrip('\s').rstrip(' ')
        q = q.replace(' ', '+')
        req.write('<div class="div_word" target="%s" href="%s" word="%s"></div>\n' %('Yahoo', dictYahoo+q, q))
    return

def genDB():
    return

def getDB(key=None):
    links = []
    db = os.path.dirname(os.path.realpath(__file__)) + '/db/'
    for f in os.listdir(db):
        fd = open(db+f, 'r')
        lines = fd.readlines()
        for l in lines:
            l = l.rstrip('\n')
            if key:
                if re.search(key, l):
                    links.append(l)
            else:
                links.append(l)
        fd.close()

    return links

def main():

    parser = OptionParser()
    parser.add_option("-g", help='gen', dest="gen", action="store_true", default=False)
    parser.add_option("-o", help='out', dest="out")
    parser.add_option("-k", help='key', dest="key")

    options, args = parser.parse_args()

    out = options.out or 'output.html'

    if options.gen == True:
        genDB()
    else:
        fd = open(out, "w")
        for link in getDB(options.key):
            fd.write(link+'\n')
        fd.close()

    return

if __name__ == '__main__':
    main()

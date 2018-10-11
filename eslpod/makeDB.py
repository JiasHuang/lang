#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
import glob

from optparse import OptionParser

class obj():
    def __init__(self, q, t, n=0):
        m = re.search(r'【【.*?】(.*?)】', t, re.DOTALL)
        if m:
            t = m.group(1)
        m = re.search(r'(\d+)', t)
        if m:
            n = int(m.group(1))
        self.q = q
        self.t = t
        self.n = n

def readLocal(local, buffering=-1):
    if os.path.exists(local):
        fd = open(local, 'r', buffering)
        txt = fd.read()
        fd.close()
        return txt
    return ''

def saveLocal(local, text, buffering=-1):
    fd = open(local, 'w', buffering)
    fd.write(text)
    fd.close()
    return

def makeIndexData(inputs, options):
    objs = []
    for i in inputs:
        try:
            q = os.path.basename(i).split('.')[0]
            m = re.search(r'<title>(.*?)</title>', readLocal(i), re.DOTALL)
            objs.append(obj(q, m.group(1)))
        except:
            print('Exception: ' + i)

    objs.sort(key= lambda x:x.n)

    txt = ''
    for o in objs:
        txt +=  '<li><a href="db.html?q=%s">%s</a></li>\n' %(o.q, o.t)

    local = '%s/index_data.js' %(options.output)
    textJS = 'var data = `\n%s\n`;' %(txt)
    saveLocal(local, textJS)

    return

def makeDataJS(inputs, options):
    for i in inputs:
        try:
            q = os.path.basename(i).split('.')[0]
            m = re.search(r'div class="desText">(.*?)</div>', readLocal(i), re.MULTILINE | re.DOTALL)
            desText = m.group(1)
            local = '%s/%s.js' %(options, q)
            textJS = 'var data = `\n%s\n`;' %(desText)
            saveLocal(local, textJS)
        except:
            print('Exception: ' + i)
    return

def main():

    parser = OptionParser()
    parser.add_option("-i", "--input", dest="input", action='append')
    parser.add_option("-o", "--output", dest="output")
    (options, args) = parser.parse_args()

    if len(options.input) == 0:
        print('no input')
        return

    if options.output is None:
        print('no output')
        return

    if not os.path.isdir(options.output):
        print('output not dir')
        return

    inputs = []
    for i in options.input:
        if os.path.isdir(i):
            inputs.extend(glob.glob('%s/*.html' %(i)))
        elif os.path.isfile(i):
            inputs.append(i)

    makeIndexData(inputs, options)
    makeDataJS(inputs, options)

    return

if __name__ == '__main__':
    main()

#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
import glob

from optparse import OptionParser

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

def makeDataJS(inputs, options):
    for i in inputs:
        try:
            q = os.path.basename(i).split('.')[0]
            m = re.search(r'(<div class="entry">.*?)<div class="definition-src">', readLocal(i), re.DOTALL | re.MULTILINE)
            txt = re.sub(r'<script.*?</script>', '', m.group(1), 0, re.DOTALL | re.MULTILINE)
            textJS = 'var data = `\n%s\n`;' %(txt)
            local = '%s/%s.js' %(options.output, q)
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

    makeDataJS(inputs, options)

    return

if __name__ == '__main__':
    main()

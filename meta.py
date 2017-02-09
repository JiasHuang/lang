#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
import urllib
import urllib2
import urlparse
import hashlib
import time

import conf

def search(patten, txt):
    m = re.search(patten, txt)
    if m:
        return m.group(1)
    return None

def readLocal(local):
    with open(local, 'r') as fd:
        return fd.read()
    return ''

def saveLocal(text, local):
    fd = open(local, 'w')
    fd.write(text)
    fd.close()
    return

def checkExpire(local):
    t0 = int(os.path.getmtime(local))
    t1 = int(time.time())
    if (t1 - t0) > 14400:
        return True
    return False

def dict2str(adict):
    return ''.join('{}{}'.format(key, val) for key, val in adict.items())

def load(url, local=None, headers=None, cache=True):

    local = local or conf.workdir+'vod_load_'+hashlib.md5(url).hexdigest()
    if cache and os.path.exists(local) and not checkExpire(local):
        return readLocal(local)

    opener = urllib2.build_opener()
    opener.addheaders = [('User-agent', 'Mozilla/5.0 (X11; Linux i686; rv:10.0) Gecko/20100101 Firefox/33.0')]

    if headers:
        opener.addheaders += headers

    try:
        f = opener.open(url, None, 10) # timeout=10
        if f.info().get('Content-Encoding') == 'gzip':
            buf = StringIO(f.read())
            txt = gzip.GzipFile(fileobj=buf).read()
        else:
            txt = f.read()
        saveLocal(txt, local)
        return txt
    except:
        return ''

def post(url, payload, local=None, cache=True):

    local = local or conf.workdir+'vod_post_'+hashlib.md5(dict2str(payload)).hexdigest()
    if cache and os.path.exists(local) and not checkExpire(local):
        return readLocal(local)

    opener = urllib2.build_opener()
    opener.addheaders = [('User-agent', 'Mozilla/5.0 (X11; Linux i686; rv:10.0) Gecko/20100101 Firefox/33.0')]
    data = urllib.urlencode(payload)
    try:
        f = opener.open(url, data)
        txt = f.read()
        saveLocal(txt, local)
        return txt
    except:
        return ''

def absURL(domain, url):
    if re.search(r'^//', url):
        return 'http:'+url
    if re.search(r'^/', url):
        return domain+url
    if not re.search(r'^http', url):
        return domain+'/'+url
    return url

def comment(req, msg):
    req.write('\n<!--\n')
    req.write(msg)
    req.write('\n-->\n')
    return


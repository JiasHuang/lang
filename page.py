#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import os
import urlparse

import mangareader
import esl
import meta

def loadFile(filename):
    path = os.path.dirname(os.path.abspath(__file__))+'/'+filename
    with open(path, 'r') as fd:
        return fd.read()
    return None

def addEntry(req, link, title, image=None):
    req.write('<div class="entry" link="%s" title="%s" image="%s"></div>\n' %(link, title or link, image or ''))
    return

def addPage(req, link, title=None, image=None):
    addEntry(req, 'lang.py?p='+link, title or link, image)
    return

def addVideo(req, src, mediatype=None):
    req.write('<div class="video" src="%s" type="%s"></div>\n' %(src, mediatype or 'video/mp4'))
    return

def addAudio(req, url):
    req.write('<div class="audio" src="%s" type="%s"></div>\n' %(url, 'audio/mpeg'))
    return

def addIFrame(req, url):
    req.write('<iframe src="%s"></iframe>\n' %(url))
    return

def page_eslpod(req, url):
    txt = meta.load(url)
    if re.search(r'/podcast/', url):
        m = re.search(r'podcast-([0-9]*)', url)
        if m:
            audio = 'https://traffic.libsyn.com/preview/secure/eslpod/DE%s.mp3' %(m.group(1))
            addAudio(req, audio)
        m = re.search(r'<div id="home" class="tab-pane fade in active">(.*?)</div>', txt, re.DOTALL|re.MULTILINE)
        if m:
            req.write('<p class="paragraph">%s</p>\n' %(m.group(1)))
            esl.parseWord(req, m.group(1))
    elif re.search(r'/library/', url):
        for m in re.finditer(r'<a href="([^"]*)">([^<]*)</a>', txt):
            link, title = m.group(1), m.group(2)
            if re.search(r'/podcast/', link):
                addPage(req, link, title)
    return

def page_dailyesl(req, url):
    txt = meta.load(url)
    if re.search(r'/$', url):
        for m in re.finditer(r'<a href="(.*?)">(.*?)</a>', txt):
            addPage(req, 'http://www.dailyesl.com/'+m.group(1), m.group(2))
        return
    for m in re.finditer(r'file: "([^"]*)"', txt):
        audio = 'http://www.dailyesl.com/'+m.group(1)
        addAudio(req, audio)
    for m in re.finditer(r'(</script>\n|</script>)</td></tr></table>(.*?)<p>', txt, re.DOTALL|re.MULTILINE):
        req.write('<p class="paragraph">%s</p>\n' %(m.group(2)))
        esl.parseWord(req, m.group(2))
    return

def page_mangareader(req, url):
    if re.search(r'/\d+$', url):
        mangareader.loadImage(req, url)
    else:
        parsed_uri = urlparse.urlparse(url)
        domain = '{uri.scheme}://{uri.netloc}'.format(uri=parsed_uri)
        for m in re.finditer(r'<a href="(.*?/\d+)">(.*?)</a>(.*?)</(li|td)>', meta.load(url)):
            link = meta.absURL(domain, m.group(1))
            title = m.group(2)+m.group(3)
            addPage(req, link, title)

def page_database(req, url):
    path = os.path.dirname(os.path.realpath(__file__)) + url
    for link in esl.getDB(path):
        addPage(req, link)
    return

def page_goodtv(req, url):
    m = re.search(r'source src="([^"]*)" type="([^"]*)"', meta.load(url))
    if m:
        addVideo(req, m.group(1), m.group(2))
    return

def page_newsinlevels(req, url):
    txt = meta.load(url)
    if re.search(r'/products/', url):
        for m in re.finditer(r'<li ><a href="(.*?)">(.*?)</a>', txt):
            link, title = m.group(1), m.group(2)
            addPage(req, link, title)
        iframeSrc = meta.search(r'<iframe.*?src="(.*?)"', txt)
        if iframeSrc:
            addIFrame(req, iframeSrc)
        content = meta.search(r'<div id="nContent">(.*?)</div>', txt, re.DOTALL|re.MULTILINE)
        if content:
            req.write(content)
            esl.parseWord(req, content)
    else:
        for m in re.finditer(r'<h3><a href="(.*?)">(.*?)</a></h3>', txt, re.DOTALL|re.MULTILINE):
            link, title = m.group(1), m.group(2)
            addPage(req, link, title)
    return

def page_bbc(req, url):
    txt = meta.load(url)
    if url.endswith('6-minute-english'):
        for m in re.finditer(r'<h2><a\s+href="(.*?)">(.*?)</a></h2>', txt):
            path, title = m.group(1), m.group(2)
            addPage(req, 'http://www.bbc.co.uk'+path, title)
    elif re.search(r'/6-minute-english/', url):
        mp3 = meta.search(r'<a class="download bbcle-download-extension-mp3" href="(.*?)">', txt)
        text = meta.search(r'<div class="text" dir="ltr">(.*?)</div>', txt, re.MULTILINE|re.DOTALL)
        if mp3:
          addAudio(req, mp3)
        if text:
          req.write('<div class="text">\n')
          req.write('\n'+text+'\n')
          req.write('</div>\n')
    return

def page(req, url):

    html = re.split('<!--result-->', loadFile('list.html'))
    req.write(html[0])

    if re.search(r'^/db/', url):
        page_database(req, url)

    elif re.search(r'eslpod', url):
        page_eslpod(req, url)

    elif re.search(r'dailyesl', url):
        page_dailyesl(req, url)

    elif re.search(r'mangareader', url):
        page_mangareader(req, url)

    elif re.search(r'goodtv', url):
        page_goodtv(req, url)

    elif re.search(r'newsinlevels', url):
        page_newsinlevels(req, url)

    elif re.search(r'bbc', url):
        page_bbc(req, url)

    req.write(html[1])
    return

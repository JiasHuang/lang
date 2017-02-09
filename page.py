#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import os

import mangareader
import esl
import meta

def loadFile(filename):
    path = os.path.dirname(os.path.abspath(__file__))+'/'+filename
    with open(path, 'r') as fd:
        return fd.read()
    return None

def addEntry(req, link, title, image=None):
    req.write('\n<a href="%s">\n' %(link))
    req.write('<h2>%s</h2>\n' %(title))
    if image:
        req.write('<img src="%s" class="img" />\n' %(image))
    req.write('</a>\n')
    return

def addPage(req, link, title, image=None):
    addEntry(req, 'lang.py?p='+link, title, image)
    return

def addVideo(req, src, mediatype):
    req.write('<video width="1280" height="720" controls>\n')
    req.write('<source src="%s" type="%s">\n' %(src, mediatype or 'video/mp4'))
    req.write('</video>\n')
    return

def addAudio(req, url):
    req.write('<hr>\n')
    req.write('<audio controls preload=none style="width:800px;"><source src="%s" type="audio/mpeg"></audio>\n' %(url))
    req.write('<hr>\n')
    return

def page_eslpod(req, url):
    txt = meta.load(url)
    if re.search(r'/podcast/', url):
        req.write('<h1><a href=%s>%s</a></h1>' %(url, url))
        m = re.search(r'podcast-([0-9]*)', url)
        if m:
            audio = 'https://traffic.libsyn.com/preview/secure/eslpod/DE%s.mp3' %(m.group(1))
            addAudio(req, audio)
        m = re.search(r'<div id="home" class="tab-pane fade in active">(.*?)</div>', txt, re.DOTALL|re.MULTILINE)
        if m:
            req.write('<font size=5><p>%s</p></font>' %(m.group(1)))
            esl.parseWord(req, m.group(1))
    elif re.search(r'/library/', url):
        for m in re.finditer(r'<a href="([^"]*)">([^<]*)</a>', txt):
            link, title = m.group(1), m.group(2)
            if re.search(r'/podcast/', link):
                addPage(req, link, title)
    return

def page_dailyesl(req, url):
    txt = meta.load(url)
    if url == 'http://www.dailyesl.com/':
        for m in re.finditer(r'<a href="(.*?)">(.*?)</a>', txt):
            addPage(req, 'http://www.dailyesl.com/'+m.group(1), m.group(2))
        return
    req.write('<h1><a href=%s>%s</a></h1>' %(url, url))
    for m in re.finditer(r'file: "([^"]*)"', txt):
        audio = 'http://www.dailyesl.com/'+m.group(1)
        addAudio(req, audio)
    for m in re.finditer(r'(</script>\n|</script>)</td></tr></table>(.*?)<p>', txt, re.DOTALL|re.MULTILINE):
        req.write('<font size=5><p>%s</p></font>' %(m.group(2)))
        esl.parseWord(req, m.group(2))
    return

def page_mangareader(req):
    txt = meta.load('http://www.mangareader.net/one-piece')
    for m in re.finditer(r'<a href="/one-piece/([^"]*)">([^"]*)</a>([^<]*)<', txt):
        link = 'http://www.mangareader.net/one-piece/'+m.group(1)
        title = m.group(2)+m.group(3)
        addPage(req, link, title)

def page_database(req):
    esl.outDB(req)
    return

def page_goodtv(req, url):
    m = re.search(r'source src="([^"]*)" type="([^"]*)"', meta.load(url))
    if m:
        addVideo(req, m.group(1), m.group(2))
    return

def page(req, url):

    html = re.split('<!--result-->', loadFile('list.html'))
    req.write(html[0])

    if url == 'mangareader':
        page_mangareader(req)

    elif url == 'database':
        page_database(req)

    elif re.search(r'eslpod', url):
        page_eslpod(req, url)

    elif re.search(r'dailyesl', url):
        page_dailyesl(req, url)

    elif re.search(r'mangareader', url):
        mangareader.loadImage(req, url)

    elif re.search(r'goodtv', url):
        page_goodtv(req, url)

    req.write(html[1])
    return

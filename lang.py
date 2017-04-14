#!/usr/bin/env python
# -*- coding: utf-8 -*-

import esl
import page

from mod_python import util

def index(req):

    req.content_type = 'text/html; charset=utf-8'

    arg = util.FieldStorage(req)

    p = arg.get('p', None)

    if p:
        page.page(req, p)

    else:
        req.write(page.loadFile('index.html'))

    return


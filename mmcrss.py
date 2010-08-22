#!/usr/bin/env python
# -*- coding:utf-8 -*-
import sys
sys.path.append('feedparser-4.1.zip')
import feedparser
from google.appengine.ext import webapp

class MMCommentRSS:
    def __init__(self):
        pass

class MMCommentRSSHandler(webapp.RequestHandler):
    def get(self):
        self.response.out.write('RSS')

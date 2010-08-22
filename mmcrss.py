#!/usr/bin/env python
# -*- coding:utf-8 -*-
import sys
sys.path.append('feedparser-4.1.zip')
import feedparser
from google.appengine.ext import webapp
from django.utils import feedgenerator

class MMCommentRSS:
    def __init__(self):
        pass

    def read(self, url):
        self.mmrss = feedparser.parse(url)

    def tostr(self):
        feed = feedgenerator.Rss201rev2Feed(
                title = self.mmrss.feed.title,
                link  = self.mmrss.feed.link,
                description = self.mmrss.feed.description,
                language = self.mmrss.feed.language
            )

        for e in self.mmrss.entries:
            feed.add_item(
                title = e.title,
                link = e.link,
                description = e.description,
            )

        return feed.writeString('utf-8')

class MMCommentRSSHandler(webapp.RequestHandler):
    def get(self):
        mmcrss = MMCommentRSS()
        mmcrss.read('http://mediamarker.net/u/sinsoku/rss')

        self.response.headers['Content-Type'] = 'text/xml; charset=utf-8'
        self.response.out.write(mmcrss.tostr())

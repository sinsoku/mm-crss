#!/usr/bin/env python
# -*- coding:utf-8 -*-
import re
from HTMLParser import HTMLParser
from zipimport import zipimporter
from google.appengine.ext import webapp
from django.utils import feedgenerator
feedparser = zipimporter('feedparser-4.1.zip').load_module('feedparser')

class ExtractCommentParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.isComment = False
        self.comment = ''

    def handle_data(self, data):
        if self.isComment:
            self.comment = data
            self.isComment = False

    def handle_startendtag(self, tag, attrs):
        if tag == "img":
            attrs = dict(attrs)
            if "title" in attrs and u'コメント' == attrs['title']:
                self.isComment = True

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
            comment = self.getComment(e)
            if comment :
                feed.add_item(
                    title = e.title,
                    link = e.link,
                    description = comment,
                )

        return feed.writeString('utf-8')

    def getComment(self, item):
        parser = ExtractCommentParser()
        parser.feed(item.description)

        return parser.comment

class MMCommentRSSHandler(webapp.RequestHandler):
    def get(self, user):
        mmcrss = MMCommentRSS()
        mmcrss.read('http://mediamarker.net/u/%s/rss' % user)

        self.response.headers['Content-Type'] = 'text/xml; charset=utf-8'
        self.response.out.write(mmcrss.tostr())

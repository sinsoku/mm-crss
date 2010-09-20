#!/usr/bin/env python
# -*- coding:utf-8 -*-
import httplib
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
        host = 'mediamarker.net'
        url = '/u/%s/rss' % user

        # ユーザのRSSがあるかチェックする
        conn = httplib.HTTPConnection(host)
        conn.request('GET', url)
        r = conn.getresponse()

        if r.getheader('Content-Type') == 'text/html':
            # RSS(xml)がない場合は'User Not Found'を表示する
            self.response.headers['Content-Type'] = 'text/html'
            self.response.out.write('User Not Found')
        else:
            # RSSがあれば、コメントのあるRSSのみ抽出して再表示する
            mmcrss = MMCommentRSS()
            mmcrss.read('http://' + host + url)
            self.response.headers['Content-Type'] = 'text/xml; charset=utf-8'
            self.response.out.write(mmcrss.tostr())

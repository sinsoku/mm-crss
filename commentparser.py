#!/usr/bin/env python
# -*- coding:utf-8 -*-
import re
from HTMLParser import HTMLParser

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

#!/usr/bin/env python
# -*- coding:utf-8 -*-
import re
from HTMLParser import HTMLParser

class ExtractCommentParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.datalist = []

    def handle_data(self, data):
        data = data.strip(" \t\r\n")
        if data:
            self.datalist.append(data)

    def handle_starttag(self, tag, attrs):
        pass

    def handle_endtag(self, tag):
        pass

    def getComment(self):
        if re.search('ISBN', self.datalist[7]) or re.search(u'詳細ページ', self.datalist[7]):
            return ''
        else:
            return self.datalist[7]

#!/usr/bin/env python
# -*- coding:utf-8 -*-
from google.appengine.ext import webapp

class MMCommentRSSHandler(webapp.RequestHandler):
    def get(self):
        self.response.out.write('RSS')

#!/usr/bin/env python
# -*- coding:utf-8 -*-
from webtest import TestApp
from main import application
from nose.tools import *

app = TestApp(application())


def test_index():
    res = app.get('/')
    assert_equal('200 OK', res.status)


def test_index_post():
    res = app.post('/', {'name': 'username'})
    assert_equal('302 Moved Temporarily', res.status)


def test_mmcrss():
    pass
    #res = app.get('/test')
    #assert_equal('200 OK', res.status)

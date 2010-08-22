#!/usr/bin/env python
# -*- coding:utf-8 -*-
from webtest import TestApp
from main import application

app = TestApp(application())

def test_index():
    response = app.get('/')
    assert 'Hello world!' in str(response)

def test_sinsoku():
    response = app.get('/sinsoku')
    assert 'RSS' in str(response)

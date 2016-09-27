# -*- coding: utf-8 -*-

import logging

class Foo(object):

    def index(self, req, resp):
        resp.body = 'I am the list view!'
        return resp

    def detail(self, req, resp, resource_id):
        resp.body = f'I am the detail view for resource: {resource_id}'
        return resp

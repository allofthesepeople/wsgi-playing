# -*- coding: utf-8 -*-

"""
Error classes, mostly for http responses
"""


class BaseHTTPError(Exception):
    def __str__(self):
        return repr(self.value)


class HTTP404Error(BaseHTTPError):
    def __init__(self, value='Not Found'):
        self.value = value
        self.status = 404
        self.msg = 'Not Found'


class HTTP500Error(BaseHTTPError):
    def __init__(self, value='Not Found'):
        self.value = value
        self.status = 500
        self.msg = 'Internal Server Error'

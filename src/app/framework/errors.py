# -*- coding: utf-8 -*-

"""
Error classes, mostly for http responses
"""


import logging


logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')


class BaseHTTPError(Exception):
    def __str__(self):
        return repr(self.value)


class HTTP404Error(BaseHTTPError):
    def __init__(self, value='Not Found'):
        self.value = value
        self.status = 404
        self.msg = 'Not Found'


class HTTP405Error(BaseHTTPError):
    def __init__(self, value='Not Found'):
        self.value = value
        self.status = 405
        self.msg = 'Method Not Allowed'


class HTTP500Error(BaseHTTPError):
    def __init__(self, value='Not Found'):
        self.value = value
        self.status = 500
        self.msg = 'Internal Server Error'
        logging.error(self)

#!/usr/bin/env python
# -*- coding: utf-8 -*-


# Stdlib

import logging
import re
from importlib import import_module
# from cgi import escape
# from cgi import parse_qs

# Local
from . import errors


logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')


VERBS = (
    'CONNECT'
    'DELETE',
    'GET',
    'HEAD',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
    'TRACE'
)


HANDLER_METHODS = (
    'create',
    'destroy',
    'detail',
    'index',
    'partial_update',
    'update',

    # Lesser used
    'connect',
    'head',
    'options',
    'trace'
)


class Request(object):
    """
    Obj to represent the request
    """
    # TODO: add all the things here

    def __init__(self, env):
        logging.critical(env)
        self.path = env.get('PATH_INFO')


class Response(object):
    """
    Obj to represent the request
    """
    # TODO: add all the things here
    pass


class App(object):
    """
    The app instance for hold app settings etc
    """

    def __init__(self, settings={}):
        self.settings = settings


    def application(self, environ, start_response):
        """
        Accepts the incoming request & throws back response from the specified
        module.
        """
        # FIXME: Meh, who needs security! Get on with it.

        # Create basic Request & Response objs
        #
        # These are then passed to the initial middleware, then altered/ignored
        # thoguh the stack
        req = Request(environ)
        resp = Response()

        try:
            req, resp = self.process(req, resp)
        except errors.BaseHTTPError as err:
            start_response(f'{err.status} {err.msg}',
                           [('Content-Type', 'application/json')])
            return [f'{err.value}'.encode()]

        start_response('200 OK', [('Content-Type', 'text/html')])

        return [b'''Hello World
        ''']

    def process(self, req, resp):
        # Router
        #
        # The router is super simple and only accepts the module name & base route
        handler, middleaware = self.compile_routes(req.path)


    #     # Load the module settings
    #
    #     # Middleware
    #     #
    #     # Loops though as `next` with req/resp params
    #     # Middleware is setup project wide but can be per module
    #     # Then spins back down again
    #     request, response = do_middleware(req, resp)
    #
    #     # Finally, return the response
    #     return response

        return req, resp

    def compile_routes(self, route):
        # get the route from the ROUTES setting
        # FIXME: resource id not accounted for
        try:
            mod_path = [r for r in self.settings.ROUTES if r[0] == route][0]
        except IndexError:
            raise errors.HTTP404Error

        logging.debug('\n\n\n\n\n\n\n\n')
        logging.debug(self.settings)
        logging.debug('\n\n\n\n\n\n\n\n')

        # now try to import the module
        # TODO: tighenup this process a little
        mod_segs = mod_path.split('.')
        handler_name = mod_segs.pop()
        mod_name = '.'.join(mod_name)

        try:
            handler = import_module(mod_name, handler_name)
        except ImportError:
            raise errors.HTTP500Error(f'{mod_path} not found')

        # Now check if the method is on the handler
        # Basically:
        # - grab the VERB
        # - split the url form the settings value:
        # - - if it is at the route level then route level applies
        # - - if there is a resource id then use it to get resource level

        return handler

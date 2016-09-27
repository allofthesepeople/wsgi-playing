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
    'TRACE',
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
        self.path = env.get('PATH_INFO')
        self.verb = env.get('REQUEST_METHOD')


class Response(object):
    """
    Obj to represent the request
    """
    # TODO: add all the things here

    headers = []
    body = ''
    status = 200


class Route(object):
    def __init__(self):
        self.func = ''
        self.kwargs = {}
        self.middleware = []


class Router(object):
    """
    Ultimately routers should be agnostic with a simple interface
    """
    _routes = {}
    VERB_MAP = {
        'CONTAINER-CONNECT': '',
        'CONTAINER-GET': 'index',
        'CONTAINER-HEAD': '',
        'CONTAINER-OPTIONS': '',
        'CONTAINER-POST': 'create',
        'CONTAINER-TRACE': '',
        'RESOURCE-CONNECT: '''
        'RESOURCE-DELETE': 'destroy',
        'RESOURCE-GET': 'detail',
        'RESOURCE-HEAD': '',
        'RESOURCE-OPTIONS': '',
        'RESOURCE-PATCH': 'partial_update',
        'RESOURCE-PUT': 'update',
        'RESOURCE-TRACE': '',
    }

    def add(self, route, resource_handler):
        """
        Fill in all blanks for the resource & add to `_routes` dict
        """
        self._routes[route] = resource_handler

    def get_route(self, req):
        route = Router()

        cls_name, resource_id = self._split_path(req.path)
        cls = self._get_cls(cls_name)
        route.func = self._get_cls_method(cls, req.verb, resource_id)
        route.kwargs = {'resource_id': resource_id} if resource_id else {}

        return route

    def _split_path(self, path):
        # TODO: split off the trailing slash

        try:
            cls_name = self._routes[path]
            resource_id = None
        except KeyError:
            path, resource_id = path.rsplit('/', maxsplit=1)

        try:
            cls_name = self._routes[path]
        except KeyError:
            logging.critical(path)
            raise errors.HTTP404Error

        return cls_name, resource_id

    def _get_cls(self, cls_path):
        cls_path, cls_name = cls_path.rsplit('.', maxsplit=1)

        try:
            module = import_module(cls_path)
            return getattr(module, cls_name)
        except (AttributeError, ImportError):
            raise errors.HTTP500Error(f"{cls_path}.{cls_name} not found.")

    def _get_cls_method(self, cls, verb, resouce_id=None):
        preface = 'RESOURCE' if resouce_id else 'CONTAINER'
        cls_method = self.VERB_MAP[f"{preface}-{verb}"]
        try:
            return getattr(cls, cls_method)
        except AttributeError:
            raise errors.HTTP405Error


class App(object):
    """
    The app instance for hold app settings etc
    """

    _routes = {}

    def __init__(self, settings={}):
        self.router = Router()
        self.settings = settings

    def __call__(self, environ, start_response):
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

        return [f"{resp.body}\n".encode()]


    def process(self, req, resp):
        # Router
        #
        # The router is super simple and only accepts the module name & base route
        # hander_cls, resource_id = self.router.get_handler_cls(req.path)
        # handler = self.router.get_handler_func()
        # handler, middleaware = self.compile_routes(req.path)
        route = self.router.get_route(req)

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

        resp = route.func(route.func, req, resp, **route.kwargs)

        return req, resp

    def compile_routes(self, route):
        # get the route from the ROUTES setting
        # FIXME: resource id not accounted for


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

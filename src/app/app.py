#! /usr/bin/env python
# -*- coding: utf-8 -*-

# Framework
from framework.app import App

# Local
import settings

app = App(settings)



if __name__ == '__main__':
    from livereload import Server, shell  # NOQA

    server = Server(app.application)
    server.serve(port=5000, host='0.0.0.0', debug=True)

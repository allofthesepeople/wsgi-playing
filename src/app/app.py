#! /usr/bin/env python
# -*- coding: utf-8 -*-

# Framework
from framework.app import App


app = App()

app.router.add('/foo', 'handlers.Foo')
app.router.add('/bar', 'handlers.Bar')

if __name__ == '__main__':
    from livereload import Server, shell  # NOQA

    server = Server(app)
    server.serve(port=5000, host='0.0.0.0', debug=True)

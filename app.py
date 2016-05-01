# -*- coding: utf-8 -*-
from __future__ import (print_function, division, absolute_import, unicode_literals, )

import os

import tornado.ioloop

from src.handler import IndexHandler, FacebookCallbackHandler


application = tornado.web.Application([
    (r"/", IndexHandler),
    (r"/fb/verify", FacebookCallbackHandler),
])


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))

    application.listen(port)
    tornado.ioloop.IOLoop.instance().start()

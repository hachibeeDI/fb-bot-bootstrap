# -*- coding: utf-8 -*-

import os

import tornado.ioloop
from tornado.web import RequestHandler
# import json

verify_token = 'aaaa'


class IndexHandler(RequestHandler):
    def get(self):
        self.write('facebook bot running')


class WebHookHandler(RequestHandler):
    def get(self):
        if self.get_argument("hub.verify_token", "") == verify_token:
            self.write(self.get_argument("hub.challenge", ""))
        else:
            self.write('Error, wrong validation token')


application = tornado.web.Application([
    (r"/", IndexHandler),
    (r"/webhook", WebHookHandler),
])


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    application.listen(port)
    tornado.ioloop.IOLoop.instance().start()

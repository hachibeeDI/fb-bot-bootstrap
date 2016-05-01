# -*- coding: utf-8 -*-

import os

import tornado.ioloop
from tornado.web import RequestHandler
# import json


FB_VERIFY_TOKEN = None


class IndexHandler(RequestHandler):
    def get(self):
        self.write('facebook bot running')


class WebHookHandler(RequestHandler):
    def get(self):
        if self.get_argument("hub.verify_token", "") == FB_VERIFY_TOKEN:
            self.write(self.get_argument("hub.challenge", ""))
        else:
            self.write('Error, wrong validation token')


application = tornado.web.Application([
    (r"/", IndexHandler),
    (r"/fb/verify", WebHookHandler),
])


if __name__ == "__main__":
    FB_VERIFY_TOKEN = os.environ['FB_VERIFY_TOKEN']
    port = int(os.environ.get("PORT", 5000))
    application.listen(port)
    tornado.ioloop.IOLoop.instance().start()

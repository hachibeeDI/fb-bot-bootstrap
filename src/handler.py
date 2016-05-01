# -*- coding: utf-8 -*-
from __future__ import (print_function, division, absolute_import, unicode_literals, )

import json

from tornado.web import RequestHandler

from .env import FB_VERIFY_TOKEN
from .utils.messages import send_request, TextMessage


def conversation(txt):
    if txt == u'おい':
        return u'あ？'
    else:
        return u'お腹がすきましたね'


class IndexHandler(RequestHandler):
    def get(self):
        self.write('facebook bot running')


class FacebookCallbackHandler(RequestHandler):
    def get(self):
        '''
        verification
        '''
        if self.get_argument("hub.verify_token", "") == FB_VERIFY_TOKEN:
            self.write(self.get_argument("hub.challenge", ""))
        else:
            self.write('Error, wrong validation token')

    def post(self):
        '''
        reply callbacks
        '''
        data = json.loads(self.request.body)
        messaging_events = data["entry"][0]["messaging"]
        for event in messaging_events:
            if "message" in event and "text" in event["message"]:
                text = event["message"]["text"]
                reply = conversation(text)
                send_request(event["sender"]["id"], TextMessage(reply))

# -*- coding: utf-8 -*-

import os
import json

import requests
import tornado.ioloop
from tornado.web import RequestHandler


FB_VERIFY_TOKEN = None
PAGE_ACCESS_TOKEN = None


def send_text_message(sender, text):
    text = text or ''
    url = 'https://graph.facebook.com/v2.6/me/messages'
    headers = {'content-type': 'application/json'}
    data = {
        "recipient": {
            "id": sender
        },
        "message":  {
            "text": text
        }
    }
    params = {"access_token": PAGE_ACCESS_TOKEN}
    requests.post(url, params=params, data=json.dumps(data), headers=headers)


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
                send_text_message(event["sender"]["id"], reply)


application = tornado.web.Application([
    (r"/", IndexHandler),
    (r"/fb/verify", FacebookCallbackHandler),
])


if __name__ == "__main__":
    FB_VERIFY_TOKEN = os.environ['FB_VERIFY_TOKEN']
    PAGE_ACCESS_TOKEN = os.environ['PAGE_ACCESS_TOKEN']
    port = int(os.environ.get("PORT", 5000))

    application.listen(port)
    tornado.ioloop.IOLoop.instance().start()

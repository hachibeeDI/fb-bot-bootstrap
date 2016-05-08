# -*- coding: utf-8 -*-
from __future__ import (print_function, division, absolute_import, unicode_literals, )

import json
import requests

from ..env import PAGE_ACCESS_TOKEN


def send_request(sender, message):
    # type: (str, MessageBase) -> None
    url = 'https://graph.facebook.com/v2.6/me/messages'
    headers = {'content-type': 'application/json'}
    params = {"access_token": PAGE_ACCESS_TOKEN}
    data = {'recipient': sender, 'message': message.to_message()}
    requests.post(
        url,
        params=params,
        data=json.dumps(data),
        headers=headers
    )


class MessageBase(object):
    def __init__(self, type):
        self.type = type

    def to_message(self, sender):
        raise NotImplementedError


class TextMessage(MessageBase):
    def __init__(self, text):
        super(TextMessage, self).__init__('button')
        self.text = text

    def to_message(self):
        return json.dumps({
            "message":  {
                "text": self.text
            }
        })


class ImageMessage(MessageBase):
    def __init__(self, url):
        super(ImageMessage, self).__init__('image')
        self.url = url

    def to_message(self):
        return json.dumps({
            "message":  {
                "url": self.url
            }
        })


class ButtonMessage(MessageBase):
    '''
        "message": {
            "attachment": {
                "type": "template",
                "payload": {
                    "template_type": "button",
                    "text": "What do you want to do next?",
                    "buttons": [
                        {
                            "type": "web_url",
                            "url": "https://petersapparel.parseapp.com",
                            "title": "Show Website"
                        },
                        {
                            "type": "postback",
                            "title": "Start Chatting",
                            "payload": "USER_DEFINED_PAYLOAD"
                        }
                    ]
                }
            }
        }
    '''

    def __init__(self, title, ):
        pass

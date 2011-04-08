#!/usr/bin/python
"""A web.py application powered by gevent"""
from gevent import monkey
monkey.patch_all()
from gevent.wsgi import WSGIServer
import web
from mimerender import mimerender
import json
import urlparse

urls = ("/", "IndexHandle",
        "/api/(\w+)/?", "UserHandle",
        "/api/(\w+)/msg/?", "MsgHandle",
        "/api/(\w+)/msg/(\w+)/?", "MsgInstanceHandle",
        "/.+", "ErrorHandle")

render_json = lambda **args: json.dumps(args)
render_html = lambda **args: json.dumps(args)


data = {}  # [user_id][msg_id] = (msg, timestamp)

errors = {'bad_page': "Invalid Page!",
          'user_exist': "User Exists!",
          'user_nexist': "User Doesn't Exist!",
          'msg_nexist': "Msg Doesn't Exist!"}


class IndexHandle(object):
    @mimerender(html=render_html, json=render_json)
    def GET(self):
        return {'users': data.keys()}


class ErrorHandle(object):
    @mimerender(html=render_html, json=render_json)
    def GET(self):
        return {'error': errors['bad_page']}


class UserHandle(object):
    @mimerender(html=render_html, json=render_json)
    def GET(self, user_id):
        try:
            return {'messages': data[user_id]}
        except KeyError:
            return {'error': errors['user_nexist']}

    @mimerender(html=render_html, json=render_json)
    def POST(self, user_id):
        if user_id in data:
            return {'error': errors['user_exist']}
        data[user_id] = {}
        return {}

    @mimerender(html=render_html, json=render_json)
    def DELETE(self, user_id):
        if user_id not in data:
            return {'error': errors['user_nexist']}
        del data[user_id]
        return {}


class MsgHandle(object):
    @mimerender(html=render_html, json=render_json)
    def POST(self, user_id):
        if user_id not in data:
            return {'error': errors['user_nexist']}
        try:
            new_key = str(max(map(int, data[user_id].keys())) + 1)
        except ValueError:
            new_key = '0'
        data[user_id][new_key] = web.data()
        return {'msg_id': new_key}


class MsgInstanceHandle(object):
    @mimerender(html=render_html, json=render_json)
    def GET(self, user_id, msg_id):
        try:
            return {'message': data[user_id][msg_id]}
        except KeyError:
            return {'error': errors['msg_nexist']}

    @mimerender(html=render_html, json=render_json)
    def DELETE(self, user_id, msg_id):
        if user_id not in data:
            return {'error': errors['user_nexist']}
        if msg_id not in data[user_id]:
            return {'error': errors['msg_nexist']}
        del data[user_id][msg_id]
        return {}


if __name__ == "__main__":
    application = web.application(urls, globals()).wsgifunc()
    print 'Serving on 8089...'
    WSGIServer(('', 8089), application).serve_forever()

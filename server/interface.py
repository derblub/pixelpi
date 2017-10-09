# -*- coding: utf-8 -*-
import web
import json

from settings import *
from input import  press, release
from jinja2 import Environment, FileSystemLoader
from websocket_server import WebsocketServer


S = Settings()
urls = (
    '/', 'index',
    '/settings', 'settings',
)


# http-server ___________________
class WebInterface(web.application):

    def run(self, *middleware):
        func = self.wsgifunc(*middleware)
        server = web.httpserver.runsimple(
            func,
            (S.get('webinterface', 'ip'), int(S.get('webinterface', 'port')))
        )
        print('\033[38;5;85mstarting http server\033[0m')
        return server


class index:
    def GET(self):
        c = {
            'page': 'index',
        }
        return render_template('index.html', c)


class settings:
    def GET(self):
        c = {
            'page': 'settings',
        }
        return render_template('settings.html', c)


def render_template(template_name, context):
    extensions = context.pop('extensions', [])
    globals = context.pop('globals', {})

    jinja_env = Environment(
        loader=FileSystemLoader(os.path.join(os.path.dirname(__file__), 'templates')),
        extensions=extensions,
    )
    jinja_env.globals.update(globals)

    return jinja_env.get_template(template_name).render(context)


# ws-server ___________________
class SocketInterface:

    def __init__(self, screen):
        self.screen = screen
        self.register_server()

    def register_server(self):
        self.server = WebsocketServer(9010, host=S.get('webinterface', 'ip'))
        self.server.set_fn_new_client(self.new_client)
        self.server.set_fn_client_left(self.client_left)
        self.server.set_fn_message_received(self.message_received)

    def run(self):
        if self.server:
            self.server.run_forever()
            print('\033[38;5;75mstarting websocket server\033[0m')
            return self.server

    def tick(self):
        c = {
            'pixel': self.screen.pixel
        }
        self.server.send_message_to_all(json.dumps(c))

    # Called for every client connecting (after handshake)
    @staticmethod
    def new_client(client, server):
        print("New client connected and was given id %d" % client['id'])

    # Called for every client disconnecting
    @staticmethod
    def client_left(client, server):
        print("Client(%d) disconnected" % client['id'])

    # Called when a client sends a message
    @staticmethod
    def message_received(client, server, message):
        # print("Client(%d) said: %s" % (client['id'], message))
        data = json.loads(message)

        if data['key']:
            press(data['key'])
            release(data['key'])

        print(data)


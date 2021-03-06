# -*- coding: utf-8 -*-

import time
import web
import json

from helpers import *
from settings import *
from input import  press, release
from jinja2 import Environment, FileSystemLoader
from websocket_server import WebsocketServer


S = Settings()
urls = (
    '/', 'index'
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
            'matrix_width': int(S.get('screen', 'matrix_width')),
            'matrix_height': int(S.get('screen', 'matrix_height'))
        }
        return render_template('index.html', c)


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
        pixel = [[0 for y in range(self.screen.height)] for x in range(self.screen.width)]

        for x in range(self.screen.width):
            for y in range(self.screen.height):
                if isinstance(self.screen.pixel[x][y], int):
                    p = int_to_color(self.screen.pixel[x][y])
                else:
                    p = self.screen.pixel[x][y]
                pixel[x][y] = p
        c = {
            'pixel': pixel
        }
        self.server.send_message_to_all(json.dumps(c))
        time.sleep(0.1)

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


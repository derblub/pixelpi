# -*- coding: utf-8 -*-
import web

from settings import *
from jinja2 import Environment, FileSystemLoader
from websocket_server import WebsocketServer
from multiprocessing import Process


S = Settings()
urls = (
    '/', 'index',
    '/settings', 'settings',
)


class WebInterface(web.application):
    def run(self, *middleware):
        func = self.wsgifunc(*middleware)
        server = web.httpserver.runsimple(
            func,
            (S.get('webinterface', 'ip'), int(S.get('webinterface', 'port')))
        )
        return server


# VIEWS ___________________
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


# websocket
# Called for every client connecting (after handshake)
def ws_new_client(client, server):
    print("New client connected and was given id %d" % client['id'])
    server.send_message_to_all("Hey all, a new client has joined us")


# Called for every client disconnecting
def ws_client_left(client, server):
    print("Client(%d) disconnected" % client['id'])


# Called when a client sends a message
def ws_message_received(client, server, message):
    if len(message) > 200:
        message = message[:200]+'..'
    print("Client(%d) said: %s" % (client['id'], message))


# _______________________
def start_webpy():
    print('\033[38;5;85mstarting web server\033[0m')
    app = WebInterface(urls, globals())
    app.run()


def start_ws():
    print('\033[38;5;75mstarting websocket server\033[0m')
    ws = WebsocketServer(9010)  # port
    ws.set_fn_new_client(ws_new_client)
    ws.set_fn_client_left(ws_client_left)
    ws.set_fn_message_received(ws_message_received)
    ws.run_forever()


def start_server():
    web_server = Process(target=start_webpy)
    web_server.start()
    socket_server = Process(target=start_ws)
    socket_server.start()
    web_server.join()
    socket_server.join()


def render_template(template_name, context):
    extensions = context.pop('extensions', [])
    globals = context.pop('globals', {})

    jinja_env = Environment(
        loader=FileSystemLoader(os.path.join(os.path.dirname(__file__), 'templates')),
        extensions=extensions,
    )
    jinja_env.globals.update(globals)

    return jinja_env.get_template(template_name).render(context)

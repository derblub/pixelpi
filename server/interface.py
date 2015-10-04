# -*- coding: utf-8 -*-
import web
import settings as s

from views import render_template


class WebInterface(web.application):
    def run(self, *middleware):
        func = self.wsgifunc(*middleware)
        return web.httpserver.runsimple(func, (s.WEBINTERFACE_IP, s.WEBINTERFACE_PORT))


urls = ('/', 'index')


class index:
    def GET(self):
        return render_template('index.html')


def start_server():
    print('\033[38;5;85mstarting web-interface\033[0m')
    app = WebInterface(urls, globals())
    app.run()

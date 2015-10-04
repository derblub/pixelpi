# -*- coding: utf-8 -*-
import os
import web
import settings as s

from jinja2 import Environment, FileSystemLoader

urls = ('/', 'index')


class WebInterface(web.application):
    def run(self, *middleware):
        func = self.wsgifunc(*middleware)
        server = web.httpserver.runsimple(
            func,
            (s.WEBINTERFACE_IP, s.WEBINTERFACE_PORT)
        )
        return server


class index:
    def GET(self):
        return render_template('index.html')


def start_server():
    print('\033[38;5;85mstarting web-interface, listening on \033[38;5;196mhttp://%s:%d/\033[0m' % (s.WEBINTERFACE_IP, s.WEBINTERFACE_PORT))
    app = WebInterface(urls, globals())
    app.run()


def render_template(template_name, **context):
    extensions = context.pop('extensions', [])
    globals = context.pop('globals', {})

    jinja_env = Environment(
        loader=FileSystemLoader(os.path.join(os.path.dirname(__file__), 'templates')),
        extensions=extensions,
    )
    jinja_env.globals.update(globals)

    return jinja_env.get_template(template_name).render(context)
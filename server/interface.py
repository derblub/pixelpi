# -*- coding: utf-8 -*-
import web

from settings import *
from jinja2 import Environment, FileSystemLoader


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


# _______________________
def start_server():
    print('\033[38;5;85mstarting web-interface, listening on \033[38;5;196mhttp://%s:%d/\033[0m' % (S.get('webinterface', 'ip'), int(S.get('webinterface', 'port'))))
    app = WebInterface(urls, globals())
    app.run()


def render_template(template_name, context):
    extensions = context.pop('extensions', [])
    globals = context.pop('globals', {})

    jinja_env = Environment(
        loader=FileSystemLoader(os.path.join(os.path.dirname(__file__), 'templates')),
        extensions=extensions,
    )
    jinja_env.globals.update(globals)

    return jinja_env.get_template(template_name).render(context)

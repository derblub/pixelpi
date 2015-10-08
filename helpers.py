import os
import ConfigParser
import collections
import colorsys

from settings import *
S = Settings()


def Color(r, g, b):
    return r * 65536 + g * 256 + b


RGBColor = collections.namedtuple('RGBColor', 'r g b')


def int_to_color(c):
    b = c & 255
    g = (c >> 8) & 255
    r = (c >> 16) & 255
    return RGBColor(r, g, b)


Point = collections.namedtuple('Point', 'x y')


def hsv_to_color(hue, saturation, value):
    t = colorsys.hsv_to_rgb(hue, saturation, value)
    return Color(int(t[0] * 255), int(t[1] * 255), int(t[2] * 255))


def rgb_to_int(c):
    return Color(c.r, c.g, c.b)


def darken_color(color, factor):
    b = color & 255
    g = (color >> 8) & 255
    r = (color >> 16) & 255
    return Color(int(r * factor), int(g * factor), int(b * factor))


def read_config(config_file):
    settings = {}
    defaults = {
        'animation': {
            'hold': str(S.get('animations', 'hold')),
            'loop': 'true'
        },
        'translate': {
            'movex': '0',
            'movey': '0',
            'loop': 'true',
            'panoff': 'false',
            'nextfolder': ''
        }
    }

    if not os.path.exists(config_file) or not os.path.isfile(config_file):
        config = defaults
    else:
        settings = ConfigParser.SafeConfigParser()
        for key, value in defaults.iteritems():
            settings.add_section(key)
            for k, v in value.iteritems():
                settings.set(key, k, v)
        config = settings._sections

    config['animation']['hold'] = settings.getint('animation', 'hold')
    config['animation']['loop'] = settings.getboolean('animation', 'loop')
    config['translate']['movex'] = settings.getint('translate', 'movex')
    config['translate']['movey'] = settings.getint('translate', 'movey')
    config['translate']['loop'] = settings.getboolean('translate', 'loop')
    config['translate']['panoff'] = settings.getboolean('translate', 'panoff')
    config['translate']['nextfolder'] = settings.get('translate', 'nextfolder')

    return config

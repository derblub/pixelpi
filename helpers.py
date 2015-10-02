import os
import ConfigParser
import collections
import settings as s


Point = collections.namedtuple('Point', 'x y')

if s.SCREEN_TO_USE is 'virtual' or s.SCREEN_TO_USE is 'console':
    Color = collections.namedtuple('Color', 'r g b')
else:
    from neopixel import *


def int_to_color(c):
    b = c & 255
    g = (c >> 8) & 255
    r = (c >> 16) & 255
    return Color(r, g, b)


def read_config(config_file):
    defaults = {
        'animation': {
            'hold': str(s.HOLD),
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

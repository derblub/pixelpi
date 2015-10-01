import collections
import settings as s

if s.SCREEN_TO_USE is 'virtual' or s.SCREEN_TO_USE is 'console':
    Color = collections.namedtuple('Color', 'r g b')
else:
    from neopixel import *


def int_to_color(c):
    b = c & 255
    g = (c >> 8) & 255
    r = (c >> 16) & 255
    return Color(r, g, b)


Point = collections.namedtuple('Point', 'x y')

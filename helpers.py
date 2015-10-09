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


def translate(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) // (in_max - in_min) + out_min


def clamp(n, minn, maxn):
    return max(min(maxn, n), minn)

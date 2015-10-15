from __future__ import division
import collections
import colorsys
import math

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


def translate(x, oldmin, oldmax, newmin, newmax):
    """Remap the float x from the range oldmin-oldmax to the range newmin-newmax
    Does not clamp values that exceed min or max.
    For example, to make a sine wave that goes between 0 and 256:
        remap(math.sin(time.time()), -1, 1, 0, 256)
    """
    zero_to_one = (x - oldmin) / (oldmax - oldmin)
    return zero_to_one * (newmax - newmin) + newmin


def clamp(n, minn, maxn):
    """Restrict the float x to the range minn-maxn."""
    return max(min(maxn, n), minn)


def cos(x, offset=0, period=1, minn=0, maxx=1):
    """A cosine curve scaled to fit in a 0-1 range and 0-1 domain by default.
    offset: how much to slide the curve across the domain (should be 0-1)
    period: the length of one wave
    minn, maxx: the output range
    """
    value = math.cos((x / period - offset) * math.pi * 2) / 2 + 0.5
    return value * (maxx - minn) + minn


def contrast(color, center, mult):
    """Expand the color values by a factor of mult around the pivot value of center.
    color: an (r, g, b) tuple
    center: a float -- the fixed point
    mult: a float -- expand or contract the values around the center point
    """
    r, g, b = color
    r = (r - center) * mult + center
    g = (g - center) * mult + center
    b = (b - center) * mult + center
    return r, g, b


def clip_black_by_luminance(color, threshold):
    """If the color's luminance is less than threshold, replace it with black.

    color: an (r, g, b) tuple
    threshold: a float
    """
    r, g, b = color
    if r + g + b < threshold * 3:
        return 0, 0, 0
    return r, g, b


def clip_black_by_channels(color, threshold):
    """Replace any individual r, g, or b value less than threshold with 0.
    color: an (r, g, b) tuple
    threshold: a float
    """
    r, g, b = color
    if r < threshold:
        r = 0
    if g < threshold:
        g = 0
    if b < threshold:
        b = 0
    return r, g, b


def mod_dist(a, b, n):
    """Return the distance between floats a and b, modulo n.
    The result is always non-negative.
    For example, thinking of a clock:
    mod_dist(11, 1, 12) == 2 because you can "wrap around".
    """
    return min((a - b) % n, (b - a) % n)


def gamma(color, gamma_):
    """Apply a gamma curve to the color.  The color values should be in the range 0-1."""
    r, g, b = color
    return max(r, 0) ** gamma_, max(g, 0) ** gamma_, max(b, 0) ** gamma_

# -*- coding: utf-8 -*-


""" screen setup
"""

MATRIX_WIDTH = 16
MATRIX_HEIGHT = 16
LED_PIN = 18
LED_FREQ = 800000
LED_DMA = 5
LED_INVERT = False

""" config options
"""
BRIGHTNESS = 200
HOLD = 200


SCREEN_TO_USE = 'matrix'
PIXEL_SIZE = 15  # for virtual-screen

try:
    from local_settings import *
except ImportError, e:
    pass
import helpers
import pygame

from settings import *
from neopixel import *
S = Settings()


class Screen:
    def __init__(self,
                 width=int(S.get('screen', 'matrix_width')),
                 height=int(S.get('screen', 'matrix_height')),
                 led_pin=int(S.get('screen', 'led_pin')),
                 led_freq_hz=int(S.get('screen', 'led_freq')),
                 led_dma=int(S.get('screen', 'led_dma')),
                 led_invert=(True if S.get('screen', 'led_invert').lower() == 'true' else False),
                 led_brightness=int(S.get('screen', 'brightness'))):
        self.width = width
        self.height = height

        self.strip = Adafruit_NeoPixel(width * height, led_pin, led_freq_hz, led_dma, led_invert, led_brightness)

        pygame.display.init()  # needed for events

        try:
            self.strip.begin()
        except RuntimeError:
            print('\033[38;5;196merror: did you run it with sudo?\033[0m')

        self.pixel = [[helpers.Color(0, 0, 0) for y in range(height)] for x in range(width)]

    def clear(self, color=helpers.Color(0, 0, 0)):
        for x in range(self.width):
            for y in range(self.height):
                self.pixel[x][y] = color

    def update(self):
        for y in range(self.height):
            for x in range(self.width):
                if y % 2 == 0:
                    self.strip.setPixelColor(y * self.width + x, self.pixel[x][y])
                else:
                    self.strip.setPixelColor(y * self.width + self.width - 1 - x, self.pixel[x][y])
        self.strip.show()

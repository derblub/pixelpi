import helpers
import pygame

from settings import *

S = Settings()

instance = None


class Screen:
    def __init__(self,
                 width=int(S.get('screen', 'matrix_width')),
                 height=int(S.get('screen', 'matrix_height')),
                 led_pin=int(S.get('screen', 'led_pin')),
                 led_freq_hz=int(S.get('screen', 'led_freq')),
                 led_dma=int(S.get('screen', 'led_dma')),
                 led_invert=(True if S.get('screen', 'led_invert').lower() == 'true' else False),
                 led_brightness=int(S.get('screen', 'brightness'))):
        import neopixel as np
        self.width = width
        self.height = height

        self.strip = np.Adafruit_NeoPixel(width * height, led_pin, led_freq_hz, led_dma, led_invert, led_brightness)

        pygame.display.init()  # needed for events

        try:
            self.strip.begin()
        except RuntimeError:
            print('\033[38;5;196merror: did you run it with sudo?\033[0m')

        self.update_brightness()
        self.pixel = [[helpers.Color(0, 0, 0) for y in range(height)] for x in range(width)]

        global instance
        instance = self

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

    def update_brightness(self):
        self.strip.setBrightness(int(4 + 3.1 * (int(S.get('screen', 'brightness')) + 1) ** 2))

    def set_brightness(self, value):
        value = min(max(value, 0), 8)
        S.set('screen', 'brightness', value)
        self.update_brightness()

    def get_brightness(self):
        return int(S.get('screen', 'brightness'))

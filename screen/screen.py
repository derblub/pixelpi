from neopixel import *

import settings as s


class Screen:
    def __init__(self,
                 width=s.MATRIX_WIDTH,
                 height=s.MATRIX_HEIGHT,
                 led_pin=s.LED_PIN,
                 led_freq_hz=s.LED_FREQ,
                 led_dma=s.LED_DMA,
                 led_invert=s.LED_INVERT,
                 led_brightness=s.BRIGHTNESS):
        self.width = width
        self.height = height

        self.strip = Adafruit_NeoPixel(width * height, led_pin, led_freq_hz, led_dma, led_invert, led_brightness)
        self.strip.begin()

        self.pixel = [[Color(0, 0, 0) for y in range(height)] for x in range(width)]

    def clear(self, color=Color(0, 0, 0)):
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

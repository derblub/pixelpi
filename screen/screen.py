from abstractscreen import AbstractScreen
from settings import *

try:
    from neopixel import *
except:
    pass

S = Settings()

instance = None


class Screen(AbstractScreen):
    def __init__(self,
                 width=int(S.get('screen', 'matrix_width')),
                 height=int(S.get('screen', 'matrix_height')),
                 led_pin=int(S.get('screen', 'led_pin')),
                 led_freq_hz=int(S.get('screen', 'led_freq')),
                 led_dma=int(S.get('screen', 'led_dma')),
                 led_invert=(True if S.get('screen', 'led_invert').lower() == 'true' else False),
                 led_brightness=int(S.get('screen', 'brightness'))):
        super(Screen, self).__init__(width, height)
        led_channel = 0
        led_strip = ws.WS2811_STRIP_GRB

        self.strip = Adafruit_NeoPixel(width * height, led_pin, led_freq_hz, led_dma, led_invert, led_brightness,
                                       led_channel, led_strip)

        # pygame.display.init()  # needed for events

        try:
            self.strip.begin()
        except RuntimeError:
            print('\033[38;5;196merror: did you run it with sudo?\033[0m')

        self.update_brightness()

        global instance
        instance = self

    def update(self):

        # mirror
        mirrored = zip(*self.pixel)

        for x in range(self.width):
            for y in range(self.height):
                if y % 2 == 0:
                    # self.strip.setPixelColor(y * self.width + x, self.pixel[x][y])
                    self.strip.setPixelColor(y * self.width + x, mirrored[x][y])
                else:
                    # self.strip.setPixelColor(y * self.width + self.width - 1 - x, self.pixel[x][y])
                    self.strip.setPixelColor(y * self.width + self.width - 1 - x, mirrored[x][y])
        self.strip.show()

    def update_brightness(self):
        self.strip.setBrightness(int(4 + 3.1 * (int(S.get('screen', 'brightness')) + 1) ** 2))

    def set_brightness(self, value):

        value = min(max(value, 0), 8)
        S.set('screen', 'brightness', value)
        self.update_brightness()

    def get_brightness(self):
        return int(S.get('screen', 'brightness'))

import libs.image2ansi as image_to_ansi
import pygame
from helpers import *
from settings import *

S = Settings()

instance = None


class ConsoleScreen:
    def __init__(self,
                 width=int(S.get('screen', 'matrix_width')),
                 height=int(S.get('screen', 'matrix_height'))):
        self.width = width
        self.height = height
        self.pixel = [[Color(0, 0, 0) for y in range(height)] for x in range(width)]

        # needed for key-events
        pygame.init()
        pygame.display.set_mode((1, 1), 0, 32)  # needed to catch key-events

    def put_cursor(self, x, y):
        print "\x1b[{};{}H".format(y + 1, x + 1)

    def clear(self, color=Color(0, 0, 0)):
        for x in range(self.width):
            for y in range(self.height):
                self.pixel[x][y] = color
        print "\x1b[2J"

    def update(self):
        # Screen.clear(self)
        for y in range(self.height):
            current_line = ""
            for x in range(self.width):
                p = int_to_color(self.pixel[x][y])
                h = "%2x%2x%2x" % (p.r, p.g, p.b)
                short, rgb = image_to_ansi.rgb2short(h)

                current_line += "\033[48;5;%sm  " % short
                # current_line += "\033[38;5;%sm  " % short
                current_line += "\033[0m"

            current_line += "\n"
            self.put_cursor(1, y + 2)
            print(current_line)

    def update_brightness(self):
        pass
        # b = int(4 + 3.1 * (int(S.get('screen', 'brightness')) + 1) ** 2)
        # @TODO maybe simulate brightness

    def set_brightness(self, value):
        value = min(max(value, 0), 8)
        S.set('screen', 'brightness', value)
        self.update_brightness()

    def get_brightness(self):
        return int(S.get('screen', 'brightness'))

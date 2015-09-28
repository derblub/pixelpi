import collections
import libs.image2ansi as image_to_ansi
import pygame

Color = collections.namedtuple('Color', 'r g b')


class ConsoleScreen:
    def __init__(self, width=16, height=16):
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
                p = self.pixel[x][y]
                h = "%2x%2x%2x" % (p.r, p.g, p.b)
                short, rgb = image_to_ansi.rgb2short(h)

                current_line += "\033[48;5;%sm  " % short
                # current_line += "\033[38;5;%sm  " % short
                current_line += "\033[0m"

            current_line += "\n"
            self.put_cursor(1, y + 2)
            print(current_line)

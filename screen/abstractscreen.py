import time

from helpers import *


class AbstractScreen(object):
    def __init__(self, width=16, height=16):
        self.width = width
        self.height = height

        self.pixel = [[RGBColor(0, 0, 0) for y in range(height)] for x in range(width)]

    def clear(self, color=RGBColor(0, 0, 0)):
        self.pixel = [[color for y in range(self.height)] for x in range(self.width)]
        # for x in range(self.width):
        #     for y in range(self.height):
        #         self.pixel[x][y] = color

    def update(self):
        pass

    def fade(self, duration, fadein):
        frame = [[self.pixel[x][y] for y in range(self.height)] for x in range(self.width)]

        start = time.time()
        end = start + duration

        while time.time() < end:
            progress = (time.time() - start) / duration
            if not fadein:
                progress = 1.0 - progress
            self.pixel = [[int_to_color(darken_color(frame[x][y], progress)) for y in range(self.height)] for x in
                          range(self.width)]
            self.update()

    def fade_in(self, duration):
        self.fade(duration, True)

    def fade_out(self, duration):
        self.fade(duration, False)

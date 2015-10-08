import time
import datetime
import math

from helpers import *
from module import Module


class Clock(Module):
    def __init__(self, screen):
        super(Clock, self).__init__(screen)

    def draw_digit(self, digit, pos, color):
        
        if digit in [0, 2, 3, 4, 5, 6, 7, 8, 9]:
            self.screen.pixel[pos.x + 0][pos.y + 0] = color
        if digit in [0, 2, 3, 5, 6, 7, 8, 9, 22]:
            self.screen.pixel[pos.x + 1][pos.y + 0] = color
        if digit in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 22]:
            self.screen.pixel[pos.x + 2][pos.y + 0] = color
        if digit in [0, 4, 5, 6, 8, 9]:
            self.screen.pixel[pos.x + 0][pos.y + 1] = color
        if digit in [0, 1, 2, 3, 4, 7, 8, 9, 22]:
            self.screen.pixel[pos.x + 2][pos.y + 1] = color
        if digit in [0, 2, 4, 5, 6, 8, 9]:
            self.screen.pixel[pos.x + 0][pos.y + 2] = color
        if digit in [2, 3, 4, 5, 6, 8, 9, 22]:
            self.screen.pixel[pos.x + 1][pos.y + 2] = color
        if digit in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 22]:
            self.screen.pixel[pos.x + 2][pos.y + 2] = color
        if digit in [0, 2, 6, 8]:
            self.screen.pixel[pos.x + 0][pos.y + 3] = color
        if digit in [0, 1, 3, 4, 5, 6, 7, 8, 9]:
            self.screen.pixel[pos.x + 2][pos.y + 3] = color
        if digit in [0, 2, 3, 5, 6, 8, 9]:
            self.screen.pixel[pos.x + 0][pos.y + 4] = color
        if digit in [0, 2, 3, 5, 6, 8, 9, 22]:
            self.screen.pixel[pos.x + 1][pos.y + 4] = color
        if digit in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 22]:
            self.screen.pixel[pos.x + 2][pos.y + 4] = color
        if digit in [22]:
            self.screen.pixel[pos.x + 1][pos.y + 3] = color

    def draw_time(self, hue, colon=True):
        now = datetime.datetime.now()

        digit_color = hsv_to_color(hue, 1, 1)
        colon_color = hsv_to_color(hue, 0.8, 1)

        self.draw_digit(now.minute % 10, Point(13, 5), digit_color)
        self.draw_digit(math.floor(now.minute / 10), Point(9, 5), digit_color)

        if colon:
            self.screen.pixel[7][6] = colon_color
            self.screen.pixel[7][8] = colon_color
        else:
            self.screen.pixel[7][6] = digit_color
            self.screen.pixel[7][8] = digit_color

        self.draw_digit(now.hour % 10, Point(3, 5), digit_color)
        if math.floor(now.hour / 10) == 1:
            self.draw_digit(1, Point(-1, 5), digit_color)
        if math.floor(now.hour / 10) == 2:
            self.draw_digit(22, Point(-1, 5), digit_color)

    def draw(self, colon=True):
        self.screen.clear()

        hue = (time.clock() * 0.01) % 1

        self.draw_time(hue, colon)
        self.screen.update()

    def tick(self):
        self.draw(False)

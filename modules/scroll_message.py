import time
import pygame
import numpy as np

from PIL import Image, ImageDraw, ImageFont

from helpers import *
from modules import Module
from settings import *
S = Settings()


class ScrollMessage(Module):

    FONTDIR = 'pilfonts/'
    DEFAULT_FONT = 'timB08'
    DEFALT_SCROLL = 'left'
    DEFALT_TEXT = 'Hello, World!'
    DEFAULT_COLOR = Color(255, 255, 255)

    def __init__(self, screen,
                 text=DEFALT_TEXT,
                 color=DEFAULT_COLOR,
                 font=DEFAULT_FONT,
                 scroll=DEFALT_SCROLL,
                 y_offset=4):
        super(ScrollMessage, self).__init__(screen)

        self.d = []
        self.width = self.screen.width
        self.height = self.screen.height

        self.text = text
        self.color = color
        self.font = self.FONTDIR + font + '.pil'
        self.scroll = scroll
        self.y_offset = y_offset

        # convert text to pixel-array
        self.pixel_array = self.img()
        self.buffer = []

        self.interval = 0.04
        self.next_step = time.clock() + self.interval

        self.start()

    def img(self):
        # blank image with enough space to fith text
        im = Image.new("RGBA", (1600, 50), (0, 0, 0, 0))
        draw = ImageDraw.Draw(im)
        font = ImageFont.load(self.font)

        draw.text((0, 0), self.text, fill=self.color, font=font)
        trimmed = self.trim_image(im)

        pixels = pygame.image.frombuffer(trimmed.tobytes(), trimmed.size, trimmed.mode)
        pixel_array = np.array(pygame.PixelArray(pixels))

        # add width of one screen to padding before and after text
        # (we start scrolling off-screen)
        pixel_array_padded = np.pad(
            pixel_array,
            ((self.width, self.width), (self.y_offset, self.y_offset)),
            mode='constant'
        )

        return pixel_array_padded

    @staticmethod
    def trim_image(im):
        bbox = im.getbbox()
        im = im.crop(bbox)
        trimmed = Image.new("RGBA", im.size, (0, 0, 0, 0))
        trimmed.paste(im, (0, 0))
        return trimmed

    def move_left(self):
        p = self.pixel_array
        self.pixel_array = np.roll(p, -1, axis=0)

    def move_right(self):
        p = self.pixel_array
        self.pixel_array = np.roll(p, 1, axis=0)

    def move_down(self):
        p = self.pixel_array
        self.pixel_array = np.roll(p, 1, axis=1)

    def move_up(self):
        p = self.pixel_array
        self.pixel_array = np.roll(p, -1, axis=1)

    def draw(self):
        p = self.pixel_array
        (w, h) = p.shape

        self.screen.clear()
        for x in range(w):
            for y in range(h):
                if y < self.screen.height and x < self.screen.width:
                    # y_o = y + self.y_offset  # y with offset
                    try:
                        self.screen.pixel[x][y] = int(p[x][y])
                    except:
                        self.screen.pixel[x][y] = 0

        self.screen.update()

    def tick(self):

        if time.clock() > self.next_step:
            self.next_step += self.interval
            s = self.scroll
            if s == "left":
                self.move_left()
            elif s == "right":
                self.move_right()
            elif s == "up":
                self.move_up()
            elif s == "down":
                self.move_down()
            elif s == "up-left":
                self.move_up()
                self.move_left()
            elif s == "up-right":
                self.move_up()
                self.move_right()
            elif s == "down-left":
                self.move_down()
                self.move_left()
            elif s == "down-left":
                self.move_down()
                self.move_right()

        self.draw()
        time.sleep(.001)

    def on_start(self):
        print('\033[38;5;39mscrolling \033[38;5;208m"\033[38;5;112m' + self.text + '\033[38;5;208m"\033[0m')
        # print "shape: ", np.array(self.pixel_array).shape

import time
import pygame

from PIL import ImageFont
from PIL import Image
from PIL import ImageDraw

from module import Module
from settings import *
S = Settings()


class ScrollMessage(Module):
    def __init__(self, screen, text):
        super(ScrollMessage, self).__init__(screen)

        self.text = text
        self.font = ImageFont.truetype("/home/repos/git/pixelpi/fonts/freesansbold.ttf", 9)

        self.start()

    def tick(self):
        self.screen.clear()

        self.screen.update()
        time.sleep(.001)

    def on_start(self):
        print('\033[38;5;39mscrolling \033[38;5;208m"\033[38;5;112m' + self.text + '\033[38;5;208m"\033[0m')

import os.path
import time
import ConfigParser

import pygame.image

from helpers import *
from module import Module


class Animation(Module):
    def __init__(self, screen, folder, interval=None, autoplay=True):
        super(Animation, self).__init__(screen)

        self.frames = []
        if not folder.endswith('/'):
            folder += '/'

        self.folder = folder
        self.screen = screen

        self.imageWidth = 0
        self.imageHeight = 0
        self.offsetSpeedX = 0  # number of pixels to  x-translate each frame
        self.offsetSpeedY = 0  # number of pixels to y-translate each frame
        self.offsetX = 0  # for translating images x pixels
        self.offsetY = 0  # for translating images y pixels

        self.holdTime = 200  # millisecods to hold each .bmp frame

        try:
            if self.is_single_file():
                self.load_single()
            else:
                self.load_frames()

            if len(self.frames) == 0:
                raise Exception('No frames found in animation ' + self.folder)

            self.screen.pixel = self.frames[0]
        except Exception:
            print('Failed to load ' + folder)
            raise

        self.screen.update()
        self.config = self.load_config()

        if interval is None:
            try:
                self.interval = int(self.config['animation']['hold'])
            except KeyError:
                self.interval = self.holdTime
        else:
            self.interval = interval

        self.pos = 0
        if autoplay:
            self.start()

    def load_frames(self):
        self.frames = []
        i = 0
        while os.path.isfile(self.folder + str(i) + '.bmp'):
            try:
                bmp = pygame.image.load(self.folder + str(i) + '.bmp')

            except Exception:
                print('Error loading ' + str(i) + '.bmp from ' + self.folder)
                raise
            arr = pygame.PixelArray(bmp)
            self.imageWidth = bmp.get_width()
            self.imageHeight = bmp.get_height()

            self.build_frame(arr)

            i += 1

    def is_single_file(self):
        return os.path.isfile(self.folder + '0.bmp') and not os.path.isfile(self.folder + '1.bmp')

    def load_single(self):
        bmp = pygame.image.load(self.folder + '0.bmp')
        framecount = bmp.get_height() / 16
        arr = pygame.PixelArray(bmp)
        self.imageWidth = bmp.get_width()
        self.imageHeight = bmp.get_height()

        for index in range(framecount):
            self.build_frame(arr)

    def build_frame(self, arr):

        # setup image for x/y translation as needed
        if self.offsetSpeedX > 0:
            if bool(self.config['translate']['panoff']):
                self.offsetX = self.imageWidth * -1
            else:
                self.offsetX = self.imageWidth * -1 + 16
        elif self.offsetSpeedX < 0:
            if bool(self.config['translate']['panoff']):
                self.offsetX = 16
            else:
                self.offsetX = 0

        if self.offsetSpeedY > 0:
            if bool(self.config['translate']['panoff']):
                self.offsetY = -16
            else:
                self.offsetY = 0
        elif self.offsetSpeedY < 0:
            if bool(self.config['translate']['panoff']):
                self.offsetY = self.imageHeight
            else:
                self.offsetY = self.imageHeight - 16

        frame = []
        for x in range(self.imageWidth):
            col = []
            for y in range(self.imageHeight):
                col.append(int_to_color(arr[x, y]))
            frame.append(col)
        self.frames.append(frame)

    def load_config(self):
        cp = ConfigParser
        cfg = cp.ConfigParser()
        try:
            cfg.read(self.folder + 'config.ini')
            to_return = {
                'animation': dict(cfg.items('animation')),
                'translate': dict(cfg.items('translate'))
            }
        except cp.NoSectionError:
            to_return = {}

        return to_return

    def tick(self):
        self.pos += 1
        if self.pos >= len(self.frames):
            self.pos = 0

        self.screen.pixel = self.frames[self.pos]
        self.screen.update()
        time.sleep(self.interval / 1000.0)

    def on_start(self):
        print('\033[38;5;39mplaying \033[38;5;82m' + self.folder + '\033[0m')

    def play_once(self):
        for frame in self.frames:
            self.screen.pixel = frame
            self.screen.update()
            time.sleep(self.interval / 1000.0)

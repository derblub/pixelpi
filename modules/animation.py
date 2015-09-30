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
                self.interval = self.config['animation']['hold']
            except KeyError:
                self.interval = 100
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

            frame = [[int_to_color(arr[x, y]) for y in range(16)] for x in range(16)]
            self.frames.append(frame)

            i += 1

    def is_single_file(self):
        return os.path.isfile(self.folder + '0.bmp') and not os.path.isfile(self.folder + '1.bmp')

    def load_single(self):
        bmp = pygame.image.load(self.folder + '0.bmp')
        framecount = bmp.get_height() / 16
        arr = pygame.PixelArray(bmp)

        for index in range(framecount):
            frame = [[int_to_color(arr[x, y + 16 * index]) for y in range(16)] for x in range(16)]
            self.frames.append(frame)

    def load_config(self):
        cfg = ConfigParser.ConfigParser()
        try:
            cfg.read(self.folder + 'config.ini')
            to_return = {
                'animation': dict(cfg.items('animation')),
                'translate': dict(cfg.items('translate'))
            }
        except ConfigParser.NoSectionError:
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

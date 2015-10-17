import time

import pygame.image
import numpy as np

from module import Module
from settings import *
S = Settings()


class Animation(Module):
    def __init__(self, screen, folder, interval=None, autoplay=True):
        super(Animation, self).__init__(screen)

        self.frames = []
        self.panoff = False
        self.moveY = 0
        self.moveX = 0
        self.moveLoop = False
        if not folder.endswith('/'):
            folder += '/'
        self.folder = folder
        self.screen = screen

        self.width = 0
        self.height = 0

        self.pos = 0

        if interval is None:
            try:
                self.interval = self.config.getint('animation', 'hold')
            except:
                # print('No interval info found.')
                self.interval = int(S.get('animations', 'hold'))
        else:
            self.interval = interval

        self.config = self.load_config(self.folder)
        self.init_defaults()

        try:
            self.load_frames()
            print "width: ", self.width
            print "height: ", self.height
            print "images: ", len(self.frames)

            if len(self.frames) == 0:
                raise Exception('No frames found in animation ' + self.folder)

            # self.screen.pixel = self.frames[0]
        except Exception:
            print('Failed to load ' + folder)
            raise

        # self.screen.update()

        if autoplay:
            self.start()

    def load_frames(self):
        self.frames = []
        frame = []
        i = 0
        while os.path.isfile(self.folder + str(i) + '.bmp'):
            try:
                bmp = pygame.image.load(self.folder + str(i) + '.bmp')
            except Exception:
                print('Error loading ' + str(i) + '.bmp from ' + self.folder)
                raise
            pixel_array = pygame.PixelArray(bmp)
            (w, h) = pixel_array.shape

            frame = [[pixel_array[x, y] for y in range(h)] for x in range(w)]
            self.frames.append(frame)

            i += 1

        shape = np.array(frame).shape
        self.width = shape[0]
        self.height = shape[1]

    def is_single_file(self):
        return os.path.isfile(self.folder + '0.bmp') and not os.path.isfile(self.folder + '1.bmp')

    @staticmethod
    def load_config(folder):
        cfg = ConfigParser.ConfigParser()
        cfg.read(folder + 'config.ini')
        return cfg

    def init_defaults(self):
        # movement loop
        try:
            self.moveLoop = self.config.getboolean('translate', 'loop')
        except:
            pass

        # move animation accross screen this many pixel per frame, + or -)
        try:
            self.moveX = self.config.getint('translate', 'movex')
        except:
            pass

        try:
            self.moveY = self.config.getint('translate', 'movey')
        except:
            pass

        # beginn/end movement off screen
        try:
            self.panoff = self.config.getboolean('translate', 'panoff')
        except:
            pass

    @staticmethod
    def do_x_movement(array, move_x):
        return np.roll(array, move_x, axis=0)

    @staticmethod
    def do_y_movement(array, move_y):
        return np.roll(array, move_y, axis=1)

    def shift_frames(self):
        if self.moveX != 0:
            self.frames[self.pos] = np.roll(self.frames[self.pos], self.moveX * self.pos, axis=0)

        if self.moveY != 0:
            self.frames[self.pos] = np.roll(self.frames[self.pos], self.moveY * self.pos, axis=1)

    def tick(self):
        if self.pos >= len(self.frames):
            self.pos = 0
            # @TODO need to get rid of this.
            # @TODO frame count is not defined by image-height/16 or number of bmps alone anymore!

        # self.shift_frames()

        self.screen.pixel = self.frames[self.pos]
        self.screen.update()
        self.pos += 1
        time.sleep(self.interval / 1000.0)

    def on_start(self):
        print('\033[38;5;39mplaying \033[38;5;82m' + self.folder + '\033[0m')

    def play_once(self):
        for frame in self.frames:
            self.screen.pixel = frame
            self.screen.update()
            time.sleep(self.interval / 1000.0)

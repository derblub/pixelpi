# -*- coding: utf-8 -*-
import time
import numpy as np

from PIL import Image
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
        self.folder = folder if folder.endswith('/') else folder + '/'
        self.screen = screen

        self.w = 0
        self.h = 0

        self.offset_x = 0
        self.offset_y = 0

        self.current_file = 0

        if interval is None:
            try:
                self.interval = self.config.getint('animation', 'hold')
            except:
                self.interval = int(S.get('animations', 'hold'))
        else:
            self.interval = interval

        self.config = self.load_config(self.folder)
        self.init_defaults()

        try:
            self.load_images()

            if len(self.frames) == 0:
                raise Exception('No frames found in animation ' + self.folder)

            # self.screen.pixel = self.frames[0]
        except Exception:
            print('Failed to load ' + folder)
            raise

        # self.screen.update()

        if autoplay:
            self.start()

    def load_images(self):
        i = 0
        while os.path.isfile(self.folder + str(i) + '.bmp'):
            try:
                bmp = Image.open(self.folder + str(i) + '.bmp', 'r')
            except Exception:
                print('Error loading ' + str(i) + '.bmp from ' + self.folder)
                raise
            pixels = np.fliplr(np.rot90(np.asarray(bmp), 3))
            self.w, self.h = bmp.size

            self.frames.append(pixels.tolist())
            i += 1

    @staticmethod
    def is_single_file(folder):
        return os.path.isfile(folder + '0.bmp') and not os.path.isfile(folder + '1.bmp')

    @staticmethod
    def config_exists(folder):
        return os.path.isfile(folder + 'config.ini')

    @staticmethod
    def load_config(folder):
        try:
            cfg = ConfigParser.ConfigParser()
            cfg.read(folder + 'config.ini')
        except(ConfigParser.MissingSectionHeaderError, ConfigParser.ParsingError):
            print('Error parsing ' + folder + 'config.ini')
            cfg = False

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

    def shift_frame(self, frame):
        frame = np.array(frame, subok=True)
        ox = self.offset_x
        oy = self.offset_y

        # setup frame for x/y translation, if needed and not paused
        if self.running:
            if self.moveX > 0:
                ox = self.w * -1 if self.panoff else self.w * -1 + self.screen.width
            elif self.moveX < 0:
                ox = self.screen.width if self.panoff else 0

            if self.moveY > 0:
                oy = self.screen.height * -1 if self.panoff else 0
            elif self.moveY < 0:
                oy = self.h if self.panoff else self.h - self.screen.height
        else:
            # center frame if paused/stopped
            ox = self.w / -2 + 8
            oy = self.h / -2 - 8

        if self.is_single_file(self.folder):
            if self.moveX == 0 and self.moveY == 0:
                # stop animation
                self.stop()

        # do x/y translations
        if self.panoff:
            if ox > self.screen.width or ox < self.w * -1 or oy > self.h or oy < self.screen.height * -1:
                if self.moveLoop:
                    if self.moveX > 0 and ox >= self.screen.width:
                        ox = self.w * -1
                    elif self.moveX < 0 and ox <= self.w * -1:
                        ox = self.screen.width
                    if self.moveY > 0 and oy >= self.h:
                        oy = self.screen.height * -1
                    elif self.moveY < 0 and oy <= self.screen.height * -1:
                        oy = self.h
        else:
            if ox > 0 or ox < (self.w * -1 + self.screen.width) or oy > self.h - self.screen.height or oy < 0:
                if self.moveLoop:
                    if self.moveX > 0 and ox >= 0:
                        ox = self.w * -1 + self.screen.width
                    elif self.moveX < 0 and ox <= self.w - self.screen.width:
                        ox = 0
                    if self.moveY > 0 and oy >= self.h - self.screen.height:
                        oy = 0
                    elif self.moveY < 0 and oy <= 0:
                        oy = self.h - self.screen.height

        if self.moveX != 0:
            ox += self.moveX
        if self.moveY != 0:
            oy += self.moveY

        frame = np.roll(frame, ox, axis=0)  # x translations
        frame = np.roll(frame, oy, axis=1)  # y translations

        self.offset_x = ox
        self.offset_y = oy

        return frame

    def tick(self):
        # for animations with multiple images
        if self.current_file >= len(self.frames):
            self.current_file = 0

        # parse config and do frame transformations
        # shifted_f = self.shift_frame(self.frames[self.current_file])
        shifted_f = self.frames[self.current_file]

        self.screen.pixel = shifted_f
        self.screen.update()

        self.current_file += 1
        time.sleep(self.interval / 1000.0)

    def on_start(self):
        print '\033[38;5;39mplaying \033[38;5;82m' + self.folder + '\033[0m'
        print u'\033[38;5;39m╰─ \033[0mwidth:', self.w, " height:", self.h, " images:", len(self.frames)

    def play_once(self):
        for frame in self.frames:
            self.screen.pixel = frame
            self.screen.update()
            time.sleep(self.interval / 1000.0)

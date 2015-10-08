import time

import pygame.image
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
        self.config = read_config(self.folder + 'config.ini')

        self.screen = screen

        def load_frames(self):
            self.frames = []
            i = 0
            while os.path.isfile(self.folder + str(i) + '.bmp'):
                try:
                    bmp = pygame.image.load(self.folder + str(i) + '.bmp')
                except Exception:
                    print('Error loading ' + str(i) + '.bmp from ' + self.folder)
                    raise
                pixel_array = pygame.PixelArray(bmp)

                frame = [[pixel_array[x, y] for y in range(16)] for x in range(16)]
                self.frames.append(frame)

                i += 1

        def is_single_file(self):
            return os.path.isfile(self.folder + '0.bmp') and not os.path.isfile(self.folder + '1.bmp')

        def load_single(self):
            self.frames = []
            bmp = pygame.image.load(self.folder + '0.bmp')
            framecount = bmp.get_height() / 16
            pixel_array = pygame.PixelArray(bmp)

            for index in range(framecount):
                frame = [[pixel_array[x, y + 16 * index] for y in range(16)] for x in range(16)]
                self.frames.append(frame)

        def load_interval(self):
            cfg = ConfigParser.ConfigParser()
            cfg.read(self.folder + 'config.ini')
            return cfg.getint('animation', 'hold')

        self.imageWidth = 0
        self.imageHeight = 0
        # self.offsetSpeedX = self.config['translate']['movex']
        self.offsetSpeedX = 1
        self.offsetSpeedY = self.config['translate']['movey']
        self.offsetX = 0  # for translating images x pixels
        self.offsetY = 0  # for translating images y pixels

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

        if interval is None:
            self.interval = self.config['animation']['hold']
        else:
            self.interval = interval

        # setup image for x/y translation as needed
        if self.offsetSpeedX > 0:
            if self.config['translate']['panoff']:
                self.offsetX = self.imageWidth * -1
            else:
                self.offsetX = self.imageWidth * -1 + 16
        elif self.offsetSpeedX < 0:
            if self.config['translate']['panoff']:
                self.offsetX = 16
            else:
                self.offsetX = 0

        if self.offsetSpeedY > 0:
            if self.config['translate']['panoff']:
                self.offsetY = -16
            else:
                self.offsetY = 0
        elif self.offsetSpeedY < 0:
            if self.config['translate']['panoff']:
                self.offsetY = self.imageHeight
            else:
                self.offsetY = self.imageHeight - 16

        self.screen.update()

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

        # begin/end movement off screen?
        if self.config['translate']['panoff']:
            if self.offsetX > 16 or self.offsetX < (self.imageWidth * -1) or self.offsetY > self.imageHeight or self.offsetY < -16:
                if self.offsetSpeedX > 0 and self.offsetX >= 16:
                    self.offsetX = (self.imageWidth * -1)
                elif self.offsetSpeedX < 0 and self.offsetX <= self.imageWidth * -1:
                    self.offsetX = 16
                if self.offsetSpeedY > 0 and self.offsetY >= self.imageHeight:
                    self.offsetY = -16
                elif self.offsetSpeedY < 0 and self.offsetY <= -16:
                    self.offsetY = self.imageHeight
        else:
            if self.offsetX > 0 or self.offsetX < (self.imageWidth * -1 + 16) or self.offsetY > self.imageHeight - 16 or self.offsetY < 0:
                if self.offsetSpeedX > 0 and self.offsetX >= 0:
                    self.offsetX = (self.imageWidth * -1 + 16)
                elif self.offsetSpeedX < 0 and self.offsetX <= self.imageWidth - 16:
                    self.offsetX = 0
                if self.offsetSpeedY > 0 and self.offsetY >= self.imageHeight - 16:
                    self.offsetY = 0
                elif self.offsetSpeedY < 0 and self.offsetY <= 0:
                    self.offsetY = self.imageHeight - 16

        if self.offsetSpeedX != 0:
            self.offsetX += self.offsetSpeedX
        if self.offsetSpeedY != 0:
            self.offsetY += self.offsetSpeedY

        frame = []
        for x in range(self.imageWidth):
            col = []
            for y in range(self.imageHeight):

                # offsetY is beyond bmp height
                if x >= self.imageHeight - self.offsetY:
                    col.append(int_to_color(0))  # black pixel
                # offsetY is negative
                elif x < self.offsetY * -1:
                    col.append(int_to_color(0))  # black pixel
                # offsetX is beyond bmp width
                elif y >= self.imageWidth + self.offsetX:
                    col.append(int_to_color(0))  # black pixel
                # offsetX is positive
                elif y < self.offsetX:
                    col.append(int_to_color(0))  # black pixel
                # all good
                else:
                    col.append(int_to_color(arr[x, y]))

            frame.append(col)
        self.frames.append(frame)

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

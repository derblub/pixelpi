import time

from fonts.font import Proportional, DEFAULT_FONT

from module import Module
from settings import *
S = Settings()


class ScrollMessage(Module):
    def __init__(self, screen, text):
        super(ScrollMessage, self).__init__(screen)

        self.text = text
        self.width = self.screen.width
        self.height = self.screen.height

        self.font = Proportional(DEFAULT_FONT).font

        self.scroll_once()

        self.pixel_array = []

        self.start()

    def scroll_once(self, direction='left'):
        length = len(self.text)
        start_range = []
        if direction == 'left':
            start_range = range(length)
        elif direction == 'right':
            start_range = range(length - 1, -1, -1)

        for start_char in start_range:
            for stage in range(8):
                for col in range(8):
                    column_data = []

                    if direction == 'left':
                        this_char = self.font[ord(self.text[start_char - 1])]
                        next_char = self.font[ord(self.text[start_char])]
                        if col + stage < 8:
                            column_data += [col + 1, this_char[col + stage]]
                        else:
                            column_data += [col + 1, next_char[col + stage - 8]]
                    elif direction == 'right':
                        this_char = self.font[ord(self.text[start_char])]
                        next_char = self.font[ord(self.text[start_char - 1])]
                        if col >= stage:
                            column_data += [col + 1, this_char[col - stage]]
                        else:
                            column_data += [col + 1, next_char[col - stage + 8]]

                    print column_data

    def tick(self):
        self.screen.clear()

        # self.screen.pixel = [[self.pixel_array[x, y + 16] for y in range(16)] for x in range(16)]

        self.screen.update()
        time.sleep(.001)

    def on_start(self):
        print('\033[38;5;39mscrolling \033[38;5;208m"\033[38;5;112m' + self.text + '\033[38;5;208m"\033[0m')

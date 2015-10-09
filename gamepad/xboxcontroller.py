import time
import pygame

from thread import start_new_thread
from pygame.locals import *

from abstractgamepad import AbstractGamepad


class Gamepad(AbstractGamepad):
    def __init__(self, verbose=False):
        super(Gamepad, self).__init__(verbose)

        # map between pygame buttons ids and xbox contorl ids
        self.BUTTONCONTROLMAP = {
            # 0: 0,  # A
            # 1: 1,  # B
            # 2: 2,  # X
            # 3: 3,  # Y
            # 4: 4,  # LB
            # 5: 5,  # RB
            6: 10,  # BACK
            7: 2,  # START
            # 8: 8,  # XBOX
            # 9: 9,  # LEFTTHUMB
            # 10: 10,  # RIGHTTHUMB
            11: 13,  # D-PAD LEFT
            12: 14,  # D-PAD RIGHT
            13: 11,  # D-PAD UP
            14: 12,  # D-PAD DOWN
        }

        pygame.joystick.init()
        joy = pygame.joystick.Joystick(0)
        joy.init()

        self.start()

    def start(self):
        self.running = True
        start_new_thread(self.run, ())

    def stop(self):
        self.running = False

    def check(self, button, pressed):
        # if the button is down its 10, if the button is up its 11
        if pressed == 10:
            self.press(int(button))
        elif pressed == 11:
            self.release(int(button))

    def run(self):
        while self.running:

            # react to the pygame events that come from the xbox controller
            for event in pygame.event.get():

                if event.type in [JOYBUTTONUP, JOYBUTTONDOWN]:
                    if event.button in self.BUTTONCONTROLMAP:
                        self.check(self.BUTTONCONTROLMAP[event.button], event.type)

        time.sleep(0.010)


if __name__ == '__main__':
    gamepad = Gamepad(verbose=True)
    while True:
        time.sleep(1)

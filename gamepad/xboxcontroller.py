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
            0: self.START,  # A
            1: self.BACK,  # B
            # 2: 2,  # X
            # 3: 3,  # Y
            # 4: 4,  # LB
            # 5: 5,  # RB
            # 6: 6,  # LT
            # 7: 7,  # RT
            8: self.BACK,  # BACK
            9: self.START,  # START
            # 10: 8,  # XBOX
            # 11: 11,  # LEFTTHUMB
            # 12: 12,  # RIGHTTHUMB
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

                # d-pad
                if event.type == JOYHATMOTION:
                    if event.value == (0, 1):
                        self.press(self.UP)
                    elif event.value == (0, -1):
                        self.press(self.DOWN)
                    elif event.value == (-1, 0):
                        self.press(self.LEFT)
                    elif event.value == (1, 0):
                        self.press(self.RIGHT)
                    elif event.value == (0, 0):
                        for btn in [self.UP, self.DOWN, self.LEFT, self.RIGHT]:
                            if self.button[btn]:
                                self.release(btn)

                # button down & up
                elif event.type in [JOYBUTTONUP, JOYBUTTONDOWN]:
                    if event.button in self.BUTTONCONTROLMAP:
                        self.check(self.BUTTONCONTROLMAP[event.button], event.type)

        time.sleep(0.010)


if __name__ == '__main__':
    gamepad = Gamepad(verbose=True)
    while True:
        time.sleep(1)

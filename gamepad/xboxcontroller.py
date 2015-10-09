import os
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
            0: 6,  # A
            1: 7,  # B
            2: 8,  # X
            3: 9,  # Y
            4: 10,  # LB
            5: 11,  # RB
            6: 12,  # BACK
            7: 13,  # START
            8: 14,  # XBOX
            9: 15,  # LEFTTHUMB
            10: 16,  # RIGHTTHUMB
        }

        # set SDL to use the dummy NULL video driver, so it doesn't need a windowing system.
        os.environ["SDL_VIDEODRIVER"] = "dummy"
        # init pygame
        pygame.init()
        # create a 1x1 pixel screen, its not used so it doesnt matter
        screen = pygame.display.set_mode((1, 1))
        # init the joystick control
        pygame.joystick.init()
        # how many joysticks are there
        # print pygame.joystick.get_count()
        # get the first joystick
        joy = pygame.joystick.Joystick(0)
        # init that joystick
        joy.init()

        # self.pipe = open('/dev/input/by-id/usb-Logitech_Logitech_Dual_Action-event-joystick', 'r')

        self.start()

    def start(self):
        self.running = True
        start_new_thread(self.run, ())

    def stop(self):
        self.running = False

    def check(self, button, pressed):
        # if the button is down its 1, if the button is up its 0
        print button, pressed
        if pressed == 1:
            self.press(int(button))
        elif pressed == 0:
            self.release(int(button))

    def run(self):
        while self.running:

            # react to the pygame events that come from the xbox controller
            for event in pygame.event.get():

                # d pad
                if event.type == JOYHATMOTION:
                    print event.value

                # button pressed and unpressed
                elif event.type == JOYBUTTONUP or event.type == JOYBUTTONDOWN:
                    if event.button in self.BUTTONCONTROLMAP:
                        self.check(event.button, event.type)

        time.sleep(0.010)


if __name__ == '__main__':
    gamepad = Gamepad(verbose=True)
    while True:
        time.sleep(1)

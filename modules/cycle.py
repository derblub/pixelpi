import os
import random

from animation import *


class Cycle(Module):
    def __init__(self, screen, location, interval=20000):
        super(Cycle, self).__init__(screen)

        self.subfolders = self.load_subfolders(location)

        self.animations = [None for i in range(len(self.subfolders))]
        self.current = None

        self.interval = interval

    def load_subfolders(self, location):

        if not location.endswith('/'):
            location += '/'

        if not os.path.exists(location):
            raise Exception("Path " + location + " not found")
        subfolders = [x[0] for x in os.walk(location)]

        subfolders = subfolders[1:]

        if len(subfolders) == 0:
            raise Exception("No animations found in " + location)

        return subfolders

    def next(self):
        if self.current is not None:
            self.current.stop()

        index = random.randint(0, len(self.animations) - 1)

        if self.animations[index] is None:
            self.animations[index] = Animation(self.screen, self.subfolders[index])

        self.current = self.animations[index]
        self.current.start()

    def tick(self):
        self.next()
        time.sleep(self.interval / 1000.0)

    def on_stop(self):
        if self.current is not None:
            self.current.stop()

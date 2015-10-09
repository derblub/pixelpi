import random

from modules.clock import Clock
from thread import start_new_thread
from animation import *
from settings import *
S = Settings()


class Cycle(Module):
    def __init__(self, screen, gamepad, location, interval=int(S.get('animations', 'show'))):
        super(Cycle, self).__init__(screen)

        self.gamepad = gamepad
        self.gamepad.on_press.append(self.key_press)

        self.subfolders = self.load_subfolders(location)

        self.animations = [None for i in range(len(self.subfolders))]

        self.show_clock = True if S.get('others', 'clock_while_cycle').lower() == 'true' else False
        self.play_count = 1
        if self.show_clock:
            self.clock = Clock(screen)

        self.interval = interval

        self.history = []
        self.history_position = -1


    @staticmethod
    def load_subfolders(location):
        if not location.endswith('/'):
            location += '/'

        if not os.path.exists(location):
            raise Exception("Path " + location + " not found")
        subfolders = [x[0] for x in os.walk(location)]

        subfolders = subfolders[1:]

        if len(subfolders) == 0:
            raise Exception("No animations found in " + location)

        return subfolders

    def get_current_animation(self):
        if self.history_position < 0:
            return None

        index = self.history[self.history_position]
        if self.animations[index] is None:
            self.animations[index] = Animation(self.screen, self.subfolders[index])
        return self.animations[index]

    def next(self, pick_random):
        if self.get_current_animation() is not None:
            self.get_current_animation().stop()

        if self.show_clock and self.play_count == int(S.get('others', 'clock_every')):
            self.play_count = 0
            start_new_thread(self.clock.start, ())
            print "showing clock"
            time.sleep(1)
            self.clock.stop()
        else:

            if self.history_position < len(self.history) - 1:
                self.history_position += 1
                index = self.history[self.history_position]
            else:
                if pick_random:
                    index = random.randint(0, len(self.animations) - 1)
                    self.history_position += 1
                else:
                    index = (self.history[self.history_position] + 1) % len(self.animations)
                    self.history_position += 1
                self.history.append(index)

            self.get_current_animation().start()

    def tick(self):
        self.next(pick_random=True)
        self.play_count += 1
        time.sleep(self.interval)

    def on_stop(self):
        if self.get_current_animation() is not None:
            self.get_current_animation().stop()

    def key_press(self, key):
        if key == self.gamepad.RIGHT:
            self.next(pick_random=False)
        if key == self.gamepad.LEFT:
            if self.history_position > 0:
                self.get_current_animation().stop()
                self.history_position -= 1
                self.get_current_animation().start()

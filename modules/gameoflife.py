import time
from random import randint
from itertools import chain

from helpers import *
from module import *


"""
Conway's Game of Life
A board is represented like this::
    {(x, y): state, ...}
...where `state` is an int from 0..2 representing a color
"""


def random_color():
    color = []
    choices = [0, 0, 48, 127, 198, 248]
    while len(color) < 3:
        color = [choices[randint(0, len(choices) - 1)] for i in range(3)]
    return Color(color[0], color[1], color[2])


class GameOfLive(Module):
    def __init__(self, screen, gamepad):
        super(GameOfLive, self).__init__(screen)
        self.gamepad = gamepad

        self.LOAD_FACTOR = 7  # smaller means more crowded
        self.NUDGING = self.LOAD_FACTOR * 1  # smaller means bigger nudge

        self.width = self.screen.width
        self.height = self.screen.height

        self.colors = self.new_colors()
        self.board = self.random_board(self.LOAD_FACTOR)
        self.detector = BoredomDetector()

        self.interval = 0.15
        self.next_step = time.clock() + self.interval

    def random_board(self, factor):
        return dict(
            ((randint(0, self.width), randint(0, self.height)), 0)
            for _ in xrange(int(self.width * self.height / factor))
        )

    @staticmethod
    def new_colors():
        c1 = random_color()
        c2 = darken_color(c1, 1.3)
        c3 = darken_color(c2, 2)
        return [c1, c2, c3]

    def next_board(self, wrap):
        """Given a board, return the board one interation later.
        Adapted from Jack Diedrich's implementation from his 2012 PyCon talk "Stop
        Writing Classes"
        :arg wrap: A callable which takes a point and transforms it, for example
            to wrap to the other edge of the screen. Return None to remove a point.
        """
        new_board = {}

        # consider only points that are alive and their neighbors:
        points_to_recalc = set(self.board.iterkeys()) | set(chain(*map(self.neighbors, self.board)))

        for point in points_to_recalc:
            count = sum((neigh in self.board) for neigh in (wrap(n) for n in self.neighbors(point) if n))

            if count == 3:
                state = 0 if point in self.board else 1
            elif count == 2 and point in self.board:
                state = 2
            else:
                state = None

            if state is not None:
                wrapped = wrap(point)
                if wrapped:
                    new_board[wrapped] = state

        return new_board

    def die(self, (x, y)):
        """Pretend any out-of-bounds cell is dead."""
        if 0 <= x < self.width and 0 <= y < self.height:
            return x, y

    @staticmethod
    def neighbors((x, y)):
        """Return the (possibly out of bounds) neighbors of a point."""
        yield x + 1, y
        yield x - 1, y
        yield x, y + 1
        yield x, y - 1
        yield x + 1, y + 1
        yield x + 1, y - 1
        yield x - 1, y + 1
        yield x - 1, y - 1

    def draw(self):
        self.screen.clear()

        for (x, y), state in self.board.iteritems():
            self.screen.pixel[x - 1][y - 1] = self.colors[state]

        self.screen.update()

    def tick(self):
        if time.clock() > self.next_step:
            self.next_step += self.interval
            self.board = self.next_board(self.die)

        # If the pattern is stuck in a loop, give it a nudge:
        if self.detector.is_bored_of(self.board):
            self.colors = self.new_colors()
            self.board.update(self.random_board(self.NUDGING))

        self.draw()
        time.sleep(.001)


class BoredomDetector(object):
    """Detector of when the simulation gets stuck in a loop"""

    # Get bored after (at minimum) this many repititions of a pattern:
    REPITITIONS = 14

    # We can detect cyclical patterns of up to this many iterations:
    PATTERN_LEN = 4

    def __init__(self):
        # Make is_bored_of() init the state the first time through:
        self.iteration = self.REPITITIONS * self.PATTERN_LEN + 1

        self.num = self.times = 0

    def is_bored_of(self, board):
        """ Return whether the simulation is probably in a loop.

        This is a stochastic guess. Basically, it detects whether the
        simulation has had the same number of cells a lot lately. May have
        false positives (like if you just have a screen full of gliders) or
        take awhile to catch on sometimes. I've even seen it totally miss the
        boat once. But it's simple and fast.
        """
        self.iteration += 1
        if len(board) == self.num:
            self.times += 1
        is_bored = self.times > self.REPITITIONS
        if self.iteration > self.REPITITIONS * self.PATTERN_LEN or is_bored:
            # A little randomness in case things divide evenly into each other:
            self.iteration = randint(-2, 0)
            self.num = len(board)
            self.times = 0

        return is_bored


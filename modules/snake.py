import random
import time

import input
from helpers import *
from modules import *


def random_color():
    color = []
    while 0 not in color or 255 not in color:
        color = [random.choice([0, 255]) for i in range(3)]
    return Color(color[0], color[1], color[2])


class Snake(Module):
    def __init__(self, screen):
        super(Snake, self).__init__(screen)

        self.snake = [Point(screen.width / 2, screen.height / 2)]
        self.dir = Point(0, -1)

        self.interval = 0.15

        self.new_game()
        input.on_press.append(self.on_key_down)

    def new_game(self):
        self.food_color = random_color()
        self.head_color = random_color()
        while self.food_color == self.head_color:
            self.head_color = random_color()

        self.snake = [Point(self.screen.width / 2, self.screen.height / 2)]
        self.dir = Point(0, -1)
        self.last_food = None

        t = 1
        start = time.clock()
        while time.clock() < start + t:
            self.screen.clear()
            self.screen.pixel[self.snake[0].x][self.snake[0].y] = darken_color(self.head_color,
                                                                               (time.clock() - start) ** 2 / t)
            self.screen.update()

        self.next_step = time.clock() + self.interval
        self.set_food()

    def game_over(self):
        print('GAME OVER - Score: ' + str(len(self.snake)))
        self.food = None
        self.draw()
        time.sleep(2)
        while len(self.snake) > 1:
            if not self.running:
                return
            self.snake = self.snake[:-1]
            self.draw()
            time.sleep(0.12)

        t = 4
        start = time.clock()
        while time.clock() < start + t:
            if not self.running:
                return
            self.screen.clear()
            self.screen.pixel[self.snake[0].x][self.snake[0].y] = darken_color(self.head_color,
                                                                               (1 - (time.clock() - start) / t) ** 2)
            self.screen.update()

        self.new_game()

    def set_food(self):
        self.food = self.snake[0]
        while self.food in self.snake:
            self.food = Point(random.randint(0, self.screen.width - 1), random.randint(0, self.screen.height - 1))
        self.pulse_offset = time.clock()

    def move(self):
        next = Point((self.snake[0].x + self.dir.x) % self.screen.width,
                     (self.snake[0].y + self.dir.y) % self.screen.height)

        if next in self.snake:
            self.game_over()
            return

        if next == self.food:
            self.last_food = self.food
            self.set_food()
            self.snake.insert(0, next)
        else:
            for i in reversed(range(1, len(self.snake))):
                self.snake[i] = self.snake[i - 1]
            self.snake[0] = next

    def draw(self):
        self.screen.clear()

        if self.food != None:
            t = 0.6
            if self.last_food != None and time.clock() - self.pulse_offset < t:
                radius = 18
                for x in range(self.screen.width):
                    for y in range(self.screen.height):
                        d = ((x - self.last_food.x) ** 2 + (y - self.last_food.y) ** 2) ** 0.5
                        if (d / radius) ** 0.5 < (time.clock() - self.pulse_offset) / t:
                            self.screen.pixel[x][y] = darken_color(self.food_color, 0.2 * (
                            1 - (time.clock() - self.pulse_offset) / t) ** 2)

        for p in self.snake:
            self.screen.pixel[p.x][p.y] = Color(255, 255, 255)
        self.screen.pixel[self.snake[0].x][self.snake[0].y] = self.head_color

        if self.food != None:
            self.screen.pixel[self.food.x][self.food.y] = darken_color(self.food_color, math.sin(
                (time.clock() - self.pulse_offset) * 8) ** 2)

        self.screen.update()

    def tick(self):
        if self.next_step < time.clock():
            self.move()
            if input.key_state[input.Key.X]:
                self.next_step += self.interval / 3
            else:
                self.next_step += self.interval
        self.draw()
        time.sleep(0.01)

    def on_key_down(self, key):
        next = self.dir
        if key == input.Key.UP:
            next = Point(0, -1)
        if key == input.Key.DOWN:
            next = Point(0, 1)
        if key == input.Key.LEFT:
            next = Point(-1, 0)
        if key == input.Key.RIGHT:
            next = Point(1, 0)

        if key == input.Key.X:
            self.next_step = time.clock()

        if len(self.snake) == 1 or self.snake[0].x + next.x != self.snake[1].x or self.snake[0].y + next.y != \
                self.snake[1].y:
            self.dir = next

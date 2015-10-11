import time
import math
import random

from helpers import *
from module import *
from modules.animation import Animation


class Ghost(object):
    ROAM = 0
    CHASE = 1
    FLEE = 2
    GOHOME = 3

    home = Point(8, 6)

    def __init__(self, game, color, initial_delay):
        self.game = game
        self.color = color
        self.pos = self.home

        self.set_mode(self.ROAM)
        self.next_move = time.clock() + initial_delay
        self.destination = None

    def get_mode_end(self):
        if self.mode == self.CHASE:
            return time.clock() + 6
        if self.mode == self.ROAM:
            return time.clock() + 10
        if self.mode == self.FLEE:
            return time.clock() + 16
        if self.mode == self.GOHOME:
            return None

    def set_mode(self, mode):
        self.mode = mode
        self.next_mode = self.get_mode_end()

    def get_next_mode(self):
        if self.mode == self.ROAM:
            return self.CHASE
        if self.mode == self.CHASE:
            return self.ROAM
        if self.mode == self.FLEE:
            return self.ROAM
        if self.mode == self.GOHOME:
            return self.ROAM

    def get_interval(self):
        if self.mode == self.CHASE:
            return 0.3
        if self.mode == self.FLEE:
            return 0.4
        if self.mode == self.ROAM:
            return 0.3
        return 0.3

    def get_random_place(self):
        p = Point(random.randint(0, 15), random.randint(0, 14))
        while self.game.walls[p.y][p.x] == 1:
            p = Point(random.randint(0, 15), random.randint(0, 14))
        return p

    def get_destination(self):
        if self.destination is not None and self.destination != self.pos:
            return self.destination

        if self.mode == self.CHASE:
            self.destination = self.game.pacman
        if self.mode == self.GOHOME:
            self.destination = self.home
        if self.mode == self.FLEE:
            self.destination = self.game.pacman
        if self.mode == self.ROAM:
            self.destination = self.get_random_place()
        return self.destination

    def get_color(self):
        if self.mode == self.FLEE:
            if self.next_mode - time.clock() < 4:
                return Color(88, 88, 221) if round(time.clock() * 5) % 2 == 0 else self.color
            return Color(88, 88, 221)
        if self.mode == self.GOHOME:
            return Color(255, 255, 255)
        return self.color

    def draw(self):
        self.game.screen.pixel[self.pos.x][self.pos.y] = self.get_color()

    def move(self):
        x = self.game.get_distance_map(self.get_destination())
        direction_map = self.game.get_direction_map(self.get_destination(), self.mode == self.FLEE)
        direction = direction_map[self.pos.x][self.pos.y]
        old = self.pos
        if direction is not None:
            self.pos = Point((self.pos.x + direction.x + 16) % 16, (self.pos.y + direction.y + 16) % 16)

    def next_mode_is_due(self):
        return ((self.next_mode is not None and self.next_mode < time.clock())
                or (self.mode == self.GOHOME and self.pos == self.home))

    def tick(self):
        if self.next_mode_is_due():
            self.set_mode(self.get_next_mode())

        if self.next_move < time.clock():
            self.next_move += self.get_interval()
            self.move()


class Pacman(Module):
    walls = [
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1],
        [1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1],
        [1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1],
        [1, 0, 0, 0, 1, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 1],
        [1, 1, 1, 0, 1, 1, 0, 0, 0, 0, 1, 1, 0, 1, 1, 1],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [1, 1, 1, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 1, 1, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1],
        [1, 0, 0, 0, 1, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 1],
        [1, 0, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    ]

    pill_spots = [Point(1, 1), Point(14, 1), Point(1, 13), Point(14, 13)]

    food_spots = [
        Point(3, 1), Point(5, 1), Point(10, 1), Point(12, 1),
        Point(1, 3), Point(3, 3), Point(5, 3), Point(10, 3), Point(12, 3), Point(14, 3),
        Point(1, 5), Point(3, 5), Point(5, 5), Point(10, 5), Point(12, 5), Point(14, 5),
        Point(1, 7), Point(3, 7), Point(5, 7), Point(10, 7), Point(12, 7), Point(14, 7),
        Point(1, 9), Point(3, 9), Point(5, 9), Point(10, 9), Point(12, 9), Point(14, 9),
        Point(1, 11), Point(3, 11), Point(5, 11), Point(10, 11), Point(12, 11), Point(14, 11),
        Point(3, 13), Point(5, 13), Point(10, 13), Point(12, 13)
    ]

    step_interval = 0.2
    wall_color = Color(0, 0, 234)
    food_color = Color(61, 44, 42)
    pill_color = Color(255, 184, 174)
    pacman_color = Color(255, 255, 0)
    cherry_color = Color(255, 0, 0)

    def __init__(self, screen, gamepad):
        super(Pacman, self).__init__(screen)
        self.gamepad = gamepad
        self.gamepad.on_press.append(self.on_key_down)

        self.new_game()

    def new_game(self):
        self.lives = 3

        self.new_level(reset_food=True)

    def new_level(self, reset_food):
        self.pacman = Point(8, 9)
        self.dir = Point(-1, 0)
        self.new_dir = self.dir
        self.next_step = time.clock() + self.step_interval + 0.8
        if reset_food:
            self.food = self.food_spots[:]
            self.pills = self.pill_spots[:]
        self.ghosts = [
            Ghost(self, Color(0, 255, 255), 2),
            Ghost(self, Color(255, 0, 0), 4),
            Ghost(self, Color(255, 184, 255), 6),
            Ghost(self, Color(255, 184, 81), 8)
        ]

    def draw_walls(self):
        for x in range(16):
            for y in range(16):
                if self.walls[y][x] == 1:
                    self.screen.pixel[x][y] = self.wall_color

    def draw(self, update=True):
        self.screen.clear()
        self.draw_walls()

        for pill in self.pills:
            self.screen.pixel[pill.x][pill.y] = self.pill_color

        for food in self.food:
            self.screen.pixel[food.x][food.y] = self.food_color

            self.screen.pixel[self.pacman.x][self.pacman.y] = darken_color(self.pacman_color, 0.2 + 0.8 * math.sin(
                time.clock() / self.step_interval / 2 * math.pi + 0.5 * math.pi) ** 2)

            for ghost in self.ghosts:
                ghost.draw()

            if update:
                self.screen.update()

    def get_nex_step(self, direction):
        return Point((self.pacman.x + direction.x + 16) % 16, (self.pacman.y + direction.y + 16) % 16)

    def move(self):
        next = self.get_nex_step(self.new_dir)

        if self.walls[next.y][next.x] == 0:
            self.pacman = next
            self.dir = self.new_dir
        else:
            next = self.get_nex_step(self.dir)
            if self.walls[next.y][next.x] == 0:
                self.pacman = next

        if self.pacman in self.food:
            self.food.remove(self.pacman)

        if self.pacman in self.pills:
            self.pills.remove(self.pacman)
            for ghost in self.ghosts:
                if ghost.mode != ghost.GOHOME:
                    ghost.set_mode(ghost.FLEE)

        if len(self.food) == 0 and len(self.pills) == 0:
            self.level_complete()

    def level_complete(self):
        animation = Animation(self.screen, "pacman/interlevel", interval=40, autoplay=False)
        animation.play_once()

        self.new_level(reset_food=True)

    def die(self):
        self.draw(update=False)
        self.screen.pixel[self.pacman.x][self.pacman.y] = self.pacman_color
        self.screen.update()

        time.sleep(1)
        start = time.clock()
        end = start + 1.5

        while time.clock() < end:
            self.draw(update=False)
            brightness = (end - time.clock()) / (end - start)
            self.screen.pixel[self.pacman.x][self.pacman.y] = Color(self.pacman_color.r * brightness,
                                                                    self.pacman_color.g * brightness,
                                                                    self.pacman_color.b * brightness)
            self.screen.update()

        time.sleep(1)
        animation = Animation(self.screen, "pacman/die", interval=100, autoplay=False)
        animation.play_once()
        time.sleep(0.5)

        self.lives -= 1
        self.new_level(reset_food=False)
        self.draw()

    def check_ghosts(self):
        for ghost in self.ghosts:
            if ghost.pos == self.pacman and ghost.pos != ghost.home:
                if ghost.mode == ghost.FLEE:
                    ghost.set_mode(ghost.GOHOME)
                elif ghost.mode != ghost.GOHOME:
                    self.die()

    def tick(self):
        for ghost in self.ghosts:
            ghost.tick()
        self.check_ghosts()

        self.draw()

        if time.clock() > self.next_step:
            self.next_step += self.step_interval
            self.move()

        time.sleep(0.005)

    def on_key_down(self, key):
        if key == self.gamepad.UP:
            self.new_dir = Point(0, -1)
        if key == self.gamepad.DOWN:
            self.new_dir = Point(0, 1)
        if key == self.gamepad.LEFT:
            self.new_dir = Point(-1, 0)
        if key == self.gamepad.RIGHT:
            self.new_dir = Point(1, 0)

    def get_distance_map(self, dest):
        directions = [Point(1, 0), Point(-1, 0), Point(0, 1), Point(0, -1)]

        to_visit = [dest]
        distance_map = [[float("inf") for y in range(16)] for x in range(16)]
        distance_map[dest.x][dest.y] = 0

        while len(to_visit) > 0:
            place = to_visit.pop()

            for direction in directions:
                next = Point((place.x + direction.x + 16) % 16, (place.y + direction.y + 16 % 16))

                if self.walls[next.y][next.x] == 0 and distance_map[next.x][next.y] > distance_map[place.x][
                    place.y] + 1:
                    distance_map[next.x][next.y] = distance_map[place.x][place.y] + 1
                    to_visit.append(next)

        return distance_map

    def get_direction_map(self, dest, invert=False):
        distance_map = self.get_distance_map(dest)
        directions_map = [[None for y in range(16)] for x in range(16)]
        directions = [Point(1, 0), Point(-1, 0), Point(0, 1), Point(0, -1)]

        for x in range(16):
            for y in range(16):
                best = 0 if invert else float("inf")
                for direction in directions:
                    next = Point((x + direction.x + 16) % 16, (y + direction.y + 16) % 16)
                    if (distance_map[next.x][next.y] > best) if invert else (distance_map[next.x][next.y] < best):
                        if self.walls[next.y][next.x] != 1:
                            directions_map[x][y] = direction
                            best = distance_map[next.x][next.y]

        return directions_map

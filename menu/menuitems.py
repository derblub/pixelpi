import os
import pygame.image

from helpers import *
if os.uname()[4][:3] == 'arm':  # if arm processor, it's most likely a rpi
    import screen.screen
else:
    import screen.virtualscreen


class MenuItem(object):
    PREVIEW_SIZE = 8

    def __init__(self):
        self.preview = None

    def get_preview(self):
        return self.preview

    def get_module(self, screen, gamepad):
        raise NotImplementedError()

    @staticmethod
    def load_preview(filename):
        bmp = pygame.image.load(filename)
        arr = pygame.PixelArray(bmp)
        frame = [[int_to_color(arr[x, y]) for y in range(MenuItem.PREVIEW_SIZE)] for x in
                 range(MenuItem.PREVIEW_SIZE)]

        return frame

    def on_key_press(self, key, menu):
        pass

    def is_launchable(self):
        return True


class CycleItem(MenuItem):
    def __init__(self):
        super(CycleItem, self).__init__()
        self.preview = MenuItem.load_preview('menu/preview/cycle.bmp')

    def get_module(self, screen, gamepad):
        from modules.cycle import Cycle
        return Cycle(screen, gamepad, 'animations')


class TetrisItem(MenuItem):
    def __init__(self):
        super(TetrisItem, self).__init__()
        self.preview = MenuItem.load_preview('menu/preview/tetris.bmp')

    def get_module(self, screen, gamepad):
        from modules.tetris import Tetris
        return Tetris(screen, gamepad)


class SnakeItem(MenuItem):
    def __init__(self):
        super(SnakeItem, self).__init__()
        self.preview = MenuItem.load_preview('menu/preview/snake.bmp')

    def get_module(self, screen, gamepad):
        from modules.snake import Snake
        return Snake(screen, gamepad)


class PacmanItem(MenuItem):
    def __init__(self):
        super(PacmanItem, self).__init__()
        self.preview = MenuItem.load_preview('menu/preview/pacman.bmp')

    def get_module(self, screen, gamepad):
        from modules.pacman import Pacman
        return Pacman(screen, gamepad)


class GameOfLifeItem(MenuItem):
    def __init__(self):
        super(GameOfLifeItem, self).__init__()
        self.preview = MenuItem.load_preview('menu/preview/gameoflife.bmp')

    def get_module(self, screen, gamepad):
        from modules.gameoflife import GameOfLive
        return GameOfLive(screen, gamepad)


class ClockItem(MenuItem):
    def __init__(self):
        super(ClockItem, self).__init__()
        self.preview = MenuItem.load_preview('menu/preview/clock.bmp')

    def get_module(self, screen, gamepad):
        from modules.clock import Clock
        return Clock(screen)


class PieItem(MenuItem):
    def __init__(self):
        super(PieItem, self).__init__()
        self.preview = MenuItem.load_preview('menu/preview/pie.bmp')

    def get_module(self, screen, gamepad):
        from modules.pie import Pie
        return Pie(screen)


class BrightnessItem(MenuItem):
    def get_module(self, screen, gamepad):
        pass

    def __init__(self, screen):
        super(BrightnessItem, self).__init__()
        self.preview_template = MenuItem.load_preview('menu/preview/brightness.bmp')
        self.screen = screen
        self.draw()

    def draw(self):
        self.preview = [self.preview_template[x][:] for x in range(8)]
        for x in range(8):
            if self.screen.get_brightness() > x:
                self.preview[x][7] = RGBColor(255, 255, 255)

    def is_launchable(self):
        return False

    def update(self, menu):
        self.draw()
        menu.draw()

    def on_key_press(self, key, menu):
        if key == menu.gamepad.UP:
            self.screen.set_brightness(self.screen.get_brightness() + 1)
            self.update(menu)
        if key == menu.gamepad.DOWN:
            self.screen.set_brightness(self.screen.get_brightness() - 1)
            self.update(menu)


class MusicItem(MenuItem):
    def __init__(self):
        super(MusicItem, self).__init__()
        self.preview = MenuItem.load_preview('menu/preview/music.bmp')

    def get_module(self, screen, gamepad):
        from modules.music import Music
        return Music(screen)


def create_menu_items():
    menu_items = [
        CycleItem(),
        TetrisItem(),
        SnakeItem(),
        PacmanItem(),
        GameOfLifeItem(),
        ClockItem(),
        PieItem(),
        MusicItem()
    ]

    if os.uname()[4][:3] == 'arm':  # if arm processor, it's most likely a rpi
        if screen.screen.instance is not None:
            menu_items.append(BrightnessItem(screen.screen.instance))
    else:
        if screen.virtualscreen.instance is not None:
            menu_items.append(BrightnessItem(screen.virtualscreen.instance))

    return menu_items

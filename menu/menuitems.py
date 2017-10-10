import platform

import pygame.image

import input
import screen.screen
import screen.virtualscreen
from helpers import *


class MenuItem(object):
    PREVIEW_SIZE = 8

    def __init__(self):
        self.preview = None

    def get_preview(self):
        return self.preview

    def get_module(self, screen):
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

    def get_module(self, screen):
        from modules.cycle import Cycle
        return Cycle(screen, 'animations')


class GalleryItem(MenuItem):
    def __init__(self):
        super(GalleryItem, self).__init__()
        self.preview = MenuItem.load_preview('menu/preview/gallery.bmp')

    def get_module(self, screen):
        from modules.gallery import Gallery
        return Gallery(screen)


class TetrisItem(MenuItem):
    def __init__(self):
        super(TetrisItem, self).__init__()
        self.preview = MenuItem.load_preview('menu/preview/tetris.bmp')

    def get_module(self, screen):
        from modules.tetris import Tetris
        return Tetris(screen)


class SnakeItem(MenuItem):
    def __init__(self):
        super(SnakeItem, self).__init__()
        self.preview = MenuItem.load_preview('menu/preview/snake.bmp')

    def get_module(self, screen):
        from modules.snake import Snake
        return Snake(screen)


class PacmanItem(MenuItem):
    def __init__(self):
        super(PacmanItem, self).__init__()
        self.preview = MenuItem.load_preview('menu/preview/pacman.bmp')

    def get_module(self, screen):
        from modules.pacman import Pacman
        return Pacman(screen)


class GameOfLifeItem(MenuItem):
    def __init__(self):
        super(GameOfLifeItem, self).__init__()
        self.preview = MenuItem.load_preview('menu/preview/gameoflife.bmp')

    def get_module(self, screen):
        from modules.gameoflife import GameOfLive
        return GameOfLive(screen)


class ClockItem(MenuItem):
    def __init__(self):
        super(ClockItem, self).__init__()
        self.preview = MenuItem.load_preview('menu/preview/clock.bmp')

    def get_module(self, screen):
        from modules.clock import Clock
        return Clock(screen)


class PieItem(MenuItem):
    def __init__(self):
        super(PieItem, self).__init__()
        self.preview = MenuItem.load_preview('menu/preview/pie.bmp')

    def get_module(self, screen):
        from modules.pie import Pie
        return Pie(screen)


class FireItem(MenuItem):
    def __init__(self):
        super(FireItem, self).__init__()
        self.preview = MenuItem.load_preview('menu/preview/fire.bmp')

    def get_module(self, screen):
        from modules.fire import Fire
        return Fire(screen)


class BrightnessItem(MenuItem):
    def __init__(self, screen):
        super(BrightnessItem, self).__init__()
        self.preview_template = MenuItem.load_preview('menu/preview/brightness.bmp')
        self.screen = screen
        self.draw()

    def get_module(self, screen):
        pass

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
        if key == input.Key.UP or key == input.Key.ENTER:
            self.screen.set_brightness(self.screen.get_brightness() + 1)
            self.update(menu)
        if key == input.Key.DOWN or key == input.Key.BACK:
            self.screen.set_brightness(self.screen.get_brightness() - 1)
            self.update(menu)


class MusicItem(MenuItem):
    def __init__(self):
        super(MusicItem, self).__init__()
        self.preview = MenuItem.load_preview('menu/preview/music.bmp')

    def get_module(self, screen):
        from modules.music import Music
        return Music(screen)


class WitnessItem(MenuItem):
    def __init__(self):
        super(WitnessItem, self).__init__()
        self.preview = MenuItem.load_preview('menu/preview/witness.bmp')

    def get_module(self, screen):
        from modules.witness import WitnessGame
        return WitnessGame(screen)


class ScrollMessageItem(MenuItem):
    def __init__(self):
        super(ScrollMessageItem, self).__init__()
        self.preview = MenuItem.load_preview('menu/preview/scrollmessage.bmp')

    def get_module(self, screen):
        from modules.scroll_message import ScrollMessage
        return ScrollMessage(screen, text="Hello, World!  :)", color=Color(255, 0, 0))


def create_menu_items():
    menu_items = [
        CycleItem(),
        GalleryItem(),
        TetrisItem(),
        SnakeItem(),
        PacmanItem(),
        GameOfLifeItem(),
        ClockItem(),
        PieItem(),
        MusicItem(),
        FireItem(),
        WitnessItem(),
        ScrollMessageItem()
    ]

    if platform.uname()[4][:3] == 'arm':  # if arm processor, it's most likely a rpi
        if screen.screen.instance is not None:
            menu_items.append(BrightnessItem(screen.screen.instance))
    else:
        if screen.virtualscreen.instance is not None:
            menu_items.append(BrightnessItem(screen.virtualscreen.instance))

    return menu_items

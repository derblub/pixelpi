import time
import thread
import pygame
import input

from menu.menuitems import create_menu_items
from screenfactory import create_screen
from server import interface
from helpers import *

os.chdir(os.path.dirname(os.path.realpath(__file__)))

S = Settings()
S.load()


class Menu(object):
    def __init__(self, screen, items):
        self.screen = screen
        input.on_press.append(self.on_key_down)

        self.index = 0
        self.MENU_ITEMS_MAP = {
            'menu': -1,
            'cycle': 0,
            'tetris': 1,
            'snake': 2,
            'pacman': 3,
            'gameoflife': 4,
            'clock': 5,
            'pie': 6,
            'music': 7,
            'scroll_message': 8,
            'brightness': 9,
        }
        self.start_screen = self.MENU_ITEMS_MAP[S.get('others', 'start_screen')]
        if self.start_screen is not -1:
            self.index += self.start_screen

        self.items = items
        self.module = None

        self.reset(redraw=False)
        if self.start_screen is -1:
            self.resume_animation()

        print("input.available_input_methods")
        print input.available_input_methods

        if self.start_screen != -1 or len(input.available_input_methods) == 0:
            self.launch()

        self.webinterface = S.get('webinterface', 'enabled')
        if self.webinterface:
            from server.interface import index
            self.http_server = interface.WebInterface(interface.urls, locals())
            thread.start_new_thread(self.http_server.run, (), {})

            self.socket_server = interface.SocketInterface(self.screen)
            thread.start_new_thread(self.socket_server.run, (), {})

    def reset(self, redraw=True):
        self.dir = 0
        self.offset = 0
        self.zoom = 1
        self.brightness = 1
        if redraw:
            self.draw()

    def draw_on_screen(self, x, y, zoom, graphic):
        if zoom == 0:
            return
        if self.brightness == 1 and zoom == 1:
            for source_x in range(8):
                for source_y in range(8):
                    target = Point(source_x + x - 4, source_y + y - 4)
                    if 0 <= target.x < 16 and 0 <= target.y < 16:
                        self.screen.pixel[target.x][target.y] = rgb_to_int(graphic[source_x][source_y])
            return

        for target_x in range(16):
            for target_y in range(16):
                source = Point(int((target_x - x) / zoom + 4), int((target_y - y) / zoom + 4))
                if 0 <= source.x < 8 and 0 <= source.y < 8:
                    c = graphic[source.x][source.y]
                    self.screen.pixel[target_x][target_y] = Color(int(c.r * self.brightness),
                                                                  int(c.g * self.brightness),
                                                                  int(c.b * self.brightness))

    def draw_scrollbar(self):
        size = int(math.floor(16 / len(self.items)))
        start = int(math.floor((16 - size) * self.index / (len(self.items) - 1)))

        for x in range(size):
            self.screen.pixel[(start + x - int(size * self.offset) + 16) % 16][15] = Color(int(80 * self.brightness),
                                                                                           int(80 * self.brightness),
                                                                                           int(80 * self.brightness))

    def draw(self):
        if self.module is not None:
            return

        self.screen.clear()
        self.draw_scrollbar()

        self.draw_on_screen(8 + int(self.offset * 12), 8, self.zoom, self.items[self.index].get_preview())

        if self.dir != 0:
            self.draw_on_screen(8 + int(self.offset * 12) - self.dir * 12, 8, self.zoom,
                                self.items[(self.index - self.dir + len(self.items)) % len(self.items)].get_preview())

        self.screen.update()

    @staticmethod
    def ease(x):
        return x

    def tick(self):
        input.tick()

        if self.socket_server:
            self.socket_server.tick()

        if self.dir != 0:
            self.offset = self.dir * self.ease((1 - (time.clock() - self.start) / (self.end - self.start)))

            if time.clock() > self.end:
                self.offset = 0
                self.dir = 0

            self.draw()

    def move(self, direction):

        self.index = (self.index + direction + len(self.items)) % len(self.items)
        self.dir = direction
        self.start = time.clock()
        self.end = self.start + 0.1

    def on_key_down(self, key):
        self.items[self.index].on_key_press(key, self)

        if self.module is not None:
            if key == input.Key.HOME or key == input.Key.BACK:
                self.stop()
            return

        if key == input.Key.RIGHT:
            self.move(1)
        if key == input.Key.LEFT:
            self.move(-1)
        if key == input.Key.ENTER or key == input.Key.A:
            self.launch()
            return True

    def stop(self):
        self.module.stop()
        self.screen.fade_out(0.3)
        self.module = None
        self.resume_animation()
        input.on_press = [self.on_key_down]
        input.on_release = []

    def launch(self):
        if not self.items[self.index].is_launchable():
            return

        self.offset = 0
        self.dir = 0

        self.start_animation()
        self.module = self.items[self.index].get_module(self.screen)
        self.module.start()

    def start_animation(self):
        start = time.clock()
        end = start + 1

        while time.clock() <= end:
            self.zoom = 1 + 16 * ((time.clock() - start) / (end - start)) ** 2
            self.brightness = min(1, 1 - ((time.clock() - start) / (end - start)))
            self.draw()

        # pygame.time.wait(100)
        time.sleep(0.1)
        self.reset(redraw=False)

    def resume_animation(self):
        start = time.clock()
        end = start + 0.5

        while time.clock() <= end:
            self.zoom = ((time.clock() - start) / (end - start))
            self.brightness = min(1, 1 * ((time.clock() - start) / (end - start)))

            self.draw()

        self.reset()


if __name__ == '__main__':
    menu = Menu(create_screen(), create_menu_items())
    while True:
        menu.tick()
        time.sleep(0.01)
        # time.sleep(0.1)

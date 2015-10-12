import pygame

from abstractscreen import AbstractScreen
from settings import *

S = Settings()

instance = None


# Behaves like the actual LED screen, but shows the screen content on a computer screen
class VirtualScreen(AbstractScreen):
    def __init__(self,
                 width=int(S.get('screen', 'matrix_width')),
                 height=int(S.get('screen', 'matrix_height'))):
        super(VirtualScreen, self).__init__(width, height)
        self.pixel_size = int(S.get('dev', 'pixel_size'))

        self.update_brightness()

        pygame.display.init()
        self.screen = pygame.display.set_mode([width * self.pixel_size, height * self.pixel_size], 0)
        self.surface = pygame.Surface(self.screen.get_size())

        global instance
        instance = self

    def update(self):
        for y in range(self.height):
            for x in range(self.width):
                pygame.draw.rect(self.surface, self.pixel[x][y], ((x * self.pixel_size, y * self.pixel_size), (((x + 1) * self.pixel_size), (y + 1) * self.pixel_size)))

        self.screen.blit(self.surface, (0, 0))
        pygame.display.flip()
        pygame.display.update()

    def update_brightness(self):
        pass
        # b = int(4 + 3.1 * (int(S.get('screen', 'brightness')) + 1) ** 2)
        # @TODO maybe simulate brightness

    def set_brightness(self, value):
        value = min(max(value, 0), 8)
        S.set('screen', 'brightness', value)
        self.update_brightness()

    def get_brightness(self):
        return int(S.get('screen', 'brightness'))

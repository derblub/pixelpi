import helpers
import pygame

from settings import *
S = Settings()

instance = None


# Behaves like the actual LED screen, but shows the screen content on a computer screen
class VirtualScreen:
    def __init__(self,
                 width=int(S.get('screen', 'matrix_width')),
                 height=int(S.get('screen', 'matrix_height'))):
        self.width = width
        self.height = height
        self.pixel_size = int(S.get('dev', 'pixel_size'))
        self.update_brightness()

        self.pixel = [[helpers.Color(0, 0, 0) for y in range(height)] for x in range(width)]

        pygame.display.init()

        self.pixel_size = int(S.get('dev', 'pixel_size'))
        self.screen = pygame.display.set_mode([width * self.pixel_size, height * self.pixel_size], 0)
        self.surface = pygame.Surface(self.screen.get_size())
        global instance
        instance = self

    def clear(self, color=helpers.Color(0, 0, 0)):
        for x in range(self.width):
            for y in range(self.height):
                self.pixel[x][y] = color

    def update(self):
        for y in range(self.height):
            for x in range(self.width):
                pygame.draw.rect(
                    self.surface,
                    self.pixel[x][y],
                    (
                        x * self.pixel_size,
                        y * self.pixel_size,
                        (x + 1) * self.pixel_size,
                        (y + 1) * self.pixel_size
                    )
                )

        self.screen.blit(self.surface, (0, 0))
        pygame.display.flip()
        pygame.display.update()

    def update_brightness(self):
        b = int(4 + 3.1 * (int(S.get('screen', 'brightness')) + 1)**2)
        # @TODO maybe simulate brightness

    def set_brightness(self, value):
        value = min(max(value, 0), 8)
        S.set('screen', 'brightness', value)
        self.update_brightness()

    def get_brightness(self):
        return int(S.get('screen', 'brightness'))

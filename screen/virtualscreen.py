import collections
import pygame
import settings as s

Color = collections.namedtuple('Color', 'r g b')


# Behaves like the actual LED screen, but shows the screen content on a computer screen
class VirtualScreen:
    def __init__(self, width=s.MATRIX_WIDTH, height=s.MATRIX_HEIGHT):
        self.width = width
        self.height = height
        self.pixel_size = s.PIXEL_SIZE

        self.pixel = [[(0, 0, 0) for y in range(height)] for x in range(width)]

        pygame.display.init()
        self.screen = pygame.display.set_mode([width * self.pixel_size, height * self.pixel_size], 0)
        self.surface = pygame.Surface(self.screen.get_size())

    def clear(self, color=(0, 0, 0)):
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

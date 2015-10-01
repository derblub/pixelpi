import pygame
import settings as s

from screenfactory import create_screen
from modules.clock import Clock

screen = create_screen()

clock = Clock(screen)
clock.start()

while True:
    pygame.time.wait(10)
    if s.SCREEN_TO_USE is 'virtual' or s.SCREEN_TO_USE is 'console':
        for event in pygame.event.get():
            pass

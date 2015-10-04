# -*- coding: utf-8 -*-
import pygame
import settings as s

from modules.cycle import Cycle
from screenfactory import create_screen


if s.WEBINTERFACE_ENABLED:
    import thread
    from server.interface import *
    thread.start_new_thread(start_server, ())


screen = create_screen()

cycle = Cycle(screen, "animations/")
cycle.start()

while True:
    pygame.time.wait(10)
    if s.SCREEN_TO_USE is 'virtual' or s.SCREEN_TO_USE is 'console':
        for event in pygame.event.get():
            pass

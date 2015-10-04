# -*- coding: utf-8 -*-
import pygame
import settings as s

from screenfactory import create_screen


if s.WEBINTERFACE_ENABLED:
    import thread
    from server.interface import *
    thread.start_new_thread(start_server, ())

screen = create_screen()

done = False
while True:
    pygame.time.wait(10)
    if s.SCREEN_TO_USE in ['virtual', 'console']:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                # quit on escape
                if (event.key == pygame.K_ESCAPE) or (event.type == pygame.QUIT):
                    done = True
                    break  # break for
        if done:
            break  # break while

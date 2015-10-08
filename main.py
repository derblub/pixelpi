# -*- coding: utf-8 -*-
import pygame

from settings import *
from screenfactory import create_screen

S = Settings()
S.load()

if S.get('webinterface', 'enabled').lower() == 'true':
    import thread
    from server.interface import *
    thread.start_new_thread(start_server, ())

screen = create_screen()

done = False
while True:
    pygame.time.wait(10)
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            # quit on escape
            if (event.key == pygame.K_ESCAPE) or (event.type == pygame.QUIT):
                done = True
                break  # break for
    if done:
        break  # break while

# -*- coding: utf-8 -*-
import sys
import random

from screenfactory import create_screen
from modules.animation import *


if s.WEBINTERFACE_ENABLED:
    import thread
    from server.interface import *
    thread.start_new_thread(start_server, ())


animations = []
for root, dirs, files in os.walk(u"animations/"):
    animations.append(root.split('/')[-1])

screen = create_screen()

if len(sys.argv) > 1:
    to_load = sys.argv[1]
else:
    to_load = u"animations/" + random.choice(animations)
animation = Animation(screen, to_load)

done = False
while True:
    pygame.time.wait(10)
    if s.SCREEN_TO_USE is 'virtual' or s.SCREEN_TO_USE is 'console':
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                # quit on escape
                if (event.key == pygame.K_ESCAPE) or (event.type == pygame.QUIT):
                    done = True
                    break  # break out from for loop
        if done:
            break  # break out from while loop

import os
import random

from screenfactory import create_screen
from modules.animation import *

animations = []
for root, dirs, files in os.walk(u"animations/"):
    animations.append(root.split('/')[-1])

screen = create_screen()

animation = Animation(screen, "animations/" + random.choice(animations))
while True:
    pygame.time.wait(10)
    for event in pygame.event.get():
        pass

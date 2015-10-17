# -*- coding: utf-8 -*-
import sys

from screenfactory import create_screen
from modules.scroll_message import *
from modules.animation import *
from helpers import *


if __name__ == '__main__':
    s = create_screen()

    # ScrollMessage(s,
    #               text="Hello, World!  :)",
    #               color=Color(255, 0, 0),
    #               scroll="left")
    Animation(s, "animations/globe")
    # Animation(s, "animations/pushingpixels")
    try:
        while True:
            pygame.time.wait(10)
    except KeyboardInterrupt:
        try:
            sys.stdout.close()
        except:
            pass
        try:
            sys.stderr.close()
        except:
            pass

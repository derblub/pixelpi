# -*- coding: utf-8 -*-
import sys

from screenfactory import create_screen
from modules.scroll_message import *
from modules.animation import *


if __name__ == '__main__':
    s = create_screen()

    # ScrollMessage(s, text="Hello, World!  :)", color=Color(255, 0, 0))

    Animation(s, "animations/globe")  # panned animation
    # Animation(s, "animations/tron_trailer")  # single image vertical animated
    # Animation(s, "animations/pushingpixels")  # single image
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

# -*- coding: utf-8 -*-

import time

from screenfactory import create_screen
from modules.scroll_message import ScrollMessage
from modules.animation import Animation


if __name__ == '__main__':
    s = create_screen()

    # ScrollMessage(s, text="Hello, World!  :)", color=Color(255, 0, 0))

    Animation(s, "animations/globe")  # panned animation
    # Animation(s, "animations/tron_trailer")  # single image vertical animated
    # Animation(s, "animations/pushingpixels")  # single image

    while True:
        time.sleep(0.01)

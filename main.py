# -*- coding: utf-8 -*-
import sys

from screenfactory import create_screen
from modules.scroll_message import *
from helpers import *


if __name__ == '__main__':
    ScrollMessage(create_screen(),
                  text="Hello, World!  :)",
                  color=Color(255, 0, 0),
                  scroll="left")
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

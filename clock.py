# -*- coding: utf-8 -*-

import time

from screenfactory import create_screen
from modules.clock import Clock


if __name__ == '__main__':
    s = create_screen()
    Clock(s)

    while True:
        time.sleep(0.01)

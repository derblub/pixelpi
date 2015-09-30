import time

from screenfactory import create_screen
from modules.clock import Clock

screen = create_screen()

clock = Clock(screen)
clock.start()

while True:
    time.sleep(10)

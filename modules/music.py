import time
import math
import audioop
from thread import start_new_thread

import alsaaudio
from helpers import *
from modules.module import Module


class Music(Module):
    def __init__(self, screen):
        super(Music, self).__init__(screen)

        # Open the device in nonblocking capture mode. The last argument could
        # just as well have been zero for blocking mode. Then we could have
        # left out the sleep call in the bottom of the loop
        self.inp = alsaaudio.PCM(alsaaudio.PCM_CAPTURE, alsaaudio.PCM_NONBLOCK)

        # Set attributes: Mono, 8000 Hz, 16 bit little endian samples
        self.inp.setchannels(1)
        self.inp.setrate(8000)
        self.inp.setformat(alsaaudio.PCM_FORMAT_S16_LE)

        # The period size controls the internal number of frames per period.
        # The significance of this parameter is documented in the ALSA api.
        # For our purposes, it is suficcient to know that reads from the device
        # will return this many frames. Each frame being 2 bytes long.
        # This means that the reads below will return either 320 bytes of data
        # or 0 bytes of data. The latter is possible because we are in nonblocking
        # mode.
        self.inp.setperiodsize(160)

        self.data = [0 for i in range(7)]
        self.position = 0
        start_new_thread(self.check_input, ())
        self.last_frame = time.time()
        self.delta_t = 0
        self.colors = [hsv_to_color(x / 16.0, 1, 1) for x in range(16)]
        self.inertia = [0 for x in range(16)]

    def check_input(self):
        while self.running:
            try:
                # read data from device
                l, data = self.inp.read()
                if l:
                    # Return the maximum of the absolute value of all samples in a fragment.
                    value = audioop.max(data, 2)
                    value = clamp(value, 80, 1023)
                    value = translate(value, 80, 1023, 0, 254)
                    # print value
                    if value == 255:
                        self.position = 0
                    elif self.position < 7:
                        self.data[self.position] = value
                        self.position += 1
                time.sleep(.001)
            except:
                pass

    def tick(self):
        self.draw()

        now = time.time()
        self.delta_t = now - self.last_frame
        self.last_frame = now

    def get_value(self, index):
        pos = index * 6.0 / 15.0
        fraction = pos % 1.0
        if fraction < 0.01:
            return self.data[int(pos)]
        lower = int(math.floor(pos))
        upper = int(math.ceil(pos))
        return self.data[lower] * fraction + self.data[upper] * (1 - fraction)

    def draw(self):
        self.screen.clear()
        for x in range(16):
            value = self.get_value(x) * 16.0 / 254.0
            for y in range(int(value)):
                self.screen.pixel[x][15 - y] = self.colors[x]
            self.inertia[x] = max(self.inertia[x], value)
            if int(self.inertia[x]) < 16:
                self.screen.pixel[x][15 - int(self.inertia[x])] = Color(255, 255, 255)
            self.inertia[x] -= self.delta_t * 15

        self.screen.update()

    def on_stop(self):
        self.inp.close()

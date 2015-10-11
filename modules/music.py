import time
import math
import audioop
import pyaudio
import struct

from thread import start_new_thread
from numpy import zeros, short, fromstring, array
from numpy.fft import fft

import alsaaudio

from helpers import *
from modules.module import Module


class Music(Module):
    def __init__(self, screen):
        super(Music, self).__init__(screen)

        p = pyaudio.PyAudio()
        self.CHUNK = 128
        self.stream = p.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=44100,
            input=True,
            frames_per_buffer=self.CHUNK
        )

        self.data = [0 for i in range(7)]
        self.position = 0
        start_new_thread(self.check_input, ())
        self.last_frame = time.time()
        self.delta_t = 0
        self.colors = [hsv_to_color(x / 16.0, 1, 1) for x in range(16)]
        self.inertia = [0 for x in range(16)]

    def check_input(self):
        from random import randint
        while self.running:
            try:
                data = fromstring(self.stream.read(self.CHUNK), dtype=short)
                # value = data / 32768.0
                value = fft(data)[1:1 + self.CHUNK / 2]

                # value = struct.unpack('h' * self.CHUNK, data)
                # value = clamp(value, 80, 1023)
                # value = translate(value, 80, 1023, 0, 254)
                # value = randint(0, 254)
                print value
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
        # self.serial.close()
        self.stream.close()

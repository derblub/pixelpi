import time
import math
import alsaaudio
import audioop
import struct
import pyaudio
import numpy

from thread import start_new_thread

from helpers import *
from modules.module import Module
from settings import *
S = Settings()


class Music(Module):
    def __init__(self, screen):
        super(Music, self).__init__(screen)

        self.data = [0 for i in range(7)]
        self.position = 0
        self.last_frame = time.time()
        self.delta_t = 0
        self.colors = [hsv_to_color(x / 16.0, 1, 1) for x in range(16)]
        self.inertia = [0 for x in range(16)]

        self.audio_input = S.get('others', 'audio_input').lower()
        if self.audio_input == 'serial':
            import serial
            self.input = serial.Serial('/dev/ttyAMA0', 9600)
            start_new_thread(self.check_serial, ())

        elif self.audio_input == 'usb_mic':
            self.CHUNK = 128
            self.p = pyaudio.PyAudio()
            self.input = self.p.open(
                format=pyaudio.paInt16,
                channels=1,
                rate=44100,
                input=True,
                frames_per_buffer=self.CHUNK
            )
            start_new_thread(self.check_levels, ())

        print "audio input: ", self.audio_input

    def check_serial(self):
        while self.running:
            try:
                byte = ord(self.input.read())
                if byte == 255:
                    self.position = 0
                elif self.position < 7:
                    self.data[self.position] = byte
                    self.position += 1
                time.sleep(.001)
            except:
                pass

    def check_levels(self):
        while self.running:
            data = self.input.read(self.CHUNK)
            print numpy.fromstring(data, numpy.int16)
            time.sleep(.001)

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
        if self.audio_input == 'serial':
            self.input.close()

        elif self.audio_input == 'usb_mic':
            self.input.stop_stream()
            self.input.close()
            self.p.terminate()

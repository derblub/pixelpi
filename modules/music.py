import time
import math
import alsaaudio
import audioop
import struct
from thread import start_new_thread

import numpy

from helpers import *
from modules.module import Module
from settings import *

S = Settings()


class Music(Module):
    def __init__(self, screen):
        super(Music, self).__init__(screen)

        self.data = [0 for i in range(8)]
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
            self.RATE = 44100
            self.CHANNELS = 2
            self.CHUNK = 512  # multiple of 16
            self.input = alsaaudio.PCM(alsaaudio.PCM_CAPTURE, alsaaudio.PCM_NORMAL)
            self.input.setchannels(self.CHANNELS)
            self.input.setrate(self.RATE)
            self.input.setformat(alsaaudio.PCM_FORMAT_S16_LE)
            self.input.setperiodsize(self.CHUNK)

            start_new_thread(self.check_levels, ())

            # print "audio input: ", self.audio_input

    @staticmethod
    def calculate_levels(data, chunk):
        # raw data to numpy array
        data = struct.unpack("%dh" % (len(data) / 2), data)
        data = numpy.array(data, dtype='h')

        # apply fft - real data so rfft used
        fourier = numpy.fft.rfft(data)
        # remove last element in array to make it the smae size as chunk
        fourier = numpy.delete(fourier, len(fourier) - 1)

        # find amplitude
        abs_p = numpy.abs(fourier)
        power = numpy.log10(abs_p.clip(min=0.0000000001)) ** 2

        # arange array matrix
        power = numpy.reshape(power, (8, chunk / 8))
        matrix = numpy.int_(numpy.average(power, axis=1) / 4)
        return matrix

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

            # read from device
            l, data = self.input.read()
            self.input.pause(1)  # pause capture whilst rpi processes data
            if l:
                # catch frame error
                try:
                    matrix = self.calculate_levels(data, self.CHUNK)
                    for i in range(7):
                        row = (1 << matrix[i]) - 1
                        row = max(0, min(row, len(matrix) - 1))
                        col = 0xFF ^ (1 << i)

                        col = clamp(col, 0, 512)
                        col = translate(col, 0, 512, 0, 255)
                        self.data[row] = col

                except audioop.error, e:
                    if e.message != "not a whole number of frames":
                        raise e

            time.sleep(.001)
            # time.sleep(.5)
            self.input.pause(0)  # resume capture

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
            self.input.close()

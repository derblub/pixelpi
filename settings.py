# -*- coding: utf-8 -*-
import os
import errno
import ConfigParser


class Settings:
    def __init__(self):
        self.defaults = self.get_defaults()
        self.filename = "settings.ini"
        self.file_handle = None

    @staticmethod
    def get_defaults():
        defaults = {
            'screen': {
                'matrix_width': '16',
                'matrix_height': '16',
                'led_pin': '18',
                'led_freq': '800000',
                'led_dma': '5',
                'led_invert': 'False',
                'brightness': '5',
            },
            'animations': {
                'show': '20',
                'hold': '100',
            },
            'webinterface': {
                'enabled': 'True',
                'ip': '0.0.0.0',
                'port': '8888',
            },
            'others': {
                ';start_screen': 'menu, [cycle], tetris, snake, pacman, gameoflife, clock, pie, music, brightness',
                'start_screen': 'cycle',

                ';clock_while_cycle': 'True, [False]',
                'clock_while_cycle': 'False',

                ';clock_every': 'int, [15]',
                'clock_every': '15',

                ';controller': 'none, xbox, logitech',
                'controller': 'none',

                ';audio_input': 'serial, [usb_mic]',
                'audio_input': 'usb_mic',
            },
            'dev': {
                ';debug': 'True, [False]',
                'debug': 'False',

                ';pixel_size': 'int, [15]',
                'pixel_size': '15',

            }
        }
        return defaults

    def put_defaults(self, file_obj):
        lb = '\n'

        header = '# delete this file to restore defaults! #'.upper()
        line = ('#' * len(header)) + lb
        file_obj.write(line + header + lb + line + lb)

        for section_name, section_value in sorted(self.defaults.iteritems()):
            file_obj.write(lb + '[' + section_name + ']' + lb)
            for setting, value in sorted(section_value.iteritems()):
                try:
                    comment = self.defaults[section_name][';' + setting]
                    file_obj.write('; ' + setting + ': ' + comment + lb)
                except KeyError:
                    comment = False
                if not setting.startswith(';'):
                    file_obj.write(setting + ' = ' + str(value) + lb)
                    if comment:
                        file_obj.write(lb)
            file_obj.write(lb)

    def get(self, section, option):
        cp = ConfigParser.SafeConfigParser(self.defaults)
        cp.read(self.filename)

        try:
            self.defaults[section]
        except KeyError:
            print 'error: no section named "%s"' % section
            quit()

        try:
            self.defaults[section][option]
        except KeyError:
            print 'error: no option named "%s" in section [%s]' % (option, section)
            quit()

        if cp.has_section(section) and cp.has_option(section, option):
            return cp.get(section, option)
        else:
            return self.defaults[section][option]

    def set(self, section, option, value):
        cp = ConfigParser.SafeConfigParser(self.defaults)
        cp.read(self.filename)
        cp.set(section, option, str(value))

        self.file_handle = os.open(self.filename, os.O_RDWR)
        with os.fdopen(self.file_handle, 'r+') as file_obj:
            file_obj.read()
            file_obj.seek(0)
            cp.write(file_obj)
            file_obj.truncate()

    def load(self):
        flags = os.O_CREAT | os.O_EXCL | os.O_WRONLY

        try:
            self.file_handle = os.open(self.filename, flags)
        except OSError as er:
            if er.errno == errno.EEXIST:  # settings exist already
                # print self.filename + " found"
                self.file_handle = os.open(self.filename, os.O_RDWR)

            else:  # something went wrong > raise exception
                print 'exception happened'
                raise
        else:  # no exception happend - file created successfully
            with os.fdopen(self.file_handle, 'w') as file_obj:
                print '%s not found - creating & writing defaults' % self.filename
                self.put_defaults(file_obj)

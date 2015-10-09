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
                'hold': '200',
            },
            'webinterface': {
                'enabled': 'True',
                'ip': '0.0.0.0',
                'port': '8888',
            },
            'others': {
                'start_screen': 'menu',
                'controller': 'xbox',
            },
            'dev': {
                'debug': 'False',
                'pixel_size': '15',

            }
        }
        return defaults

    def put_defaults(self, file_obj):
        lb = '\n'

        for section_name, section_value in sorted(self.defaults.iteritems()):
            file_obj.write('[' + section_name + ']' + lb)
            for setting, value in sorted(section_value.iteritems()):
                file_obj.write(setting + ' = ' + str(value) + lb)
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
                print self.filename + " found"
                self.file_handle = os.open(self.filename, os.O_RDWR)

            else:  # something went wrong > raise exception
                print 'exception happened'
                raise
        else:  # no exception happend - file created successfully
            with os.fdopen(self.file_handle, 'w') as file_obj:
                print self.filename + 'not found - creating & writing defaults'
                self.put_defaults(file_obj)

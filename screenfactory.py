import os, platform


def create_screen():
    if platform.uname()[4][:3] == 'arm':  # if arm processor, it's most likely a rpi
        from screen.screen import Screen
        return Screen()
    else:
        # from screen.consolescreen import ConsoleScreen
        # return ConsoleScreen()
        from screen.virtualscreen import VirtualScreen
        return VirtualScreen()

import settings as s


def create_screen():
    if s.SCREEN_TO_USE == 'virtual':
        from screen.virtualscreen import VirtualScreen
        return VirtualScreen()
    elif s.SCREEN_TO_USE == 'console':
        from screen.consolescreen import ConsoleScreen
        return ConsoleScreen()
    else:
        from screen.screen import Screen
        return Screen()

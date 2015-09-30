# Use this to switch between virtual and LED screen for examples
screen_to_use = 'virtual'


def create_screen():
    if screen_to_use == 'virtual':
        from screen.virtualscreen import VirtualScreen
        return VirtualScreen()
    elif screen_to_use == 'console':
        from screen.consolescreen import ConsoleScreen
        return ConsoleScreen()
    else:
        from screen.screen import Screen
        return Screen()

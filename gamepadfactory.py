from settings import *
S = Settings()


def create_gamepad():
    c = S.get('others', 'controller')

    if c == 'xbox':
        from gamepad.xboxcontroller import Gamepad
        return Gamepad()

    elif c == 'logitech':
        from gamepad.gamepad import Gamepad
        return Gamepad()

    else:
        from gamepad.virtualgamepad import instance
        return instance

from settings import *
S = Settings()


def create_gamepad():
    from gamepad.virtualgamepad import instance
    return instance
    # from gamepad.gamepad import Gamepad
    # return Gamepad()

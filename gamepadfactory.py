import settings as s


def create_gamepad():
    if s.INPUT_TYPE == 'virtual':
        from gamepad.virtualgamepad import instance
        return instance
    else:
        from gamepad.gamepad import Gamepad
        return Gamepad()

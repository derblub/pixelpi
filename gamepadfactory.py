def create_gamepad():
    try:
        from gamepad.virtualgamepad import instance
        return instance
    except:
        from gamepad.gamepad import Gamepad
        return Gamepad()

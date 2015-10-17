class AbstractGamepad(object):
    UP = 11
    DOWN = 12
    LEFT = 13
    RIGHT = 14
    START = 10
    BACK = 2

    btn_count = 15

    def __init__(self, verbose=False):
        self.verbose = verbose
        self.button = [False for i in range(self.btn_count)]

        self.on_press = []
        self.on_release = []

    def press(self, btn):
        try:
            self.button[btn] = True
            if self.verbose:
                print('Pressed ' + str(btn))
            for callback in self.on_press:
                event_handled = callback(btn)
                if event_handled:
                    return
        except TypeError:
            # don't crash on unexpected key-codes
            pass

    def release(self, btn):
        try:
            self.button[btn] = False
            if self.verbose:
                print('Released ' + str(btn))
            for callback in self.on_release:
                event_handled = callback(btn)
                if event_handled:
                    return
        except TypeError:
            # don't crash on unexpected key-codes
            pass

    def tick(self):
        pass

    def available(self):
        return True

    def consume_event(self, event):
        pass

import pygame

from abstractgamepad import AbstractGamepad

instance = None


class VirtualGamepad(AbstractGamepad):
    def __init__(self, verbose=False):
        super(VirtualGamepad, self).__init__(verbose)

        self.keycode_list = [
            (276, self.LEFT),
            (275, self.RIGHT),
            (273, self.UP),
            (274, self.DOWN),
            (0, 10),
            (1, 1),
            (2, 2),
            (3, 3),
            (4, 4),
            (5, 5),
            (6, 6),
            (7, 7),
            (8, 8),
            (9, 9)
        ]

        if instance is not None:
            raise Exception("Don't create multiple virtual gamepads!")

    def keycode_to_int(self, keycode):
        print keycode
        for relation in self.keycode_list:
            if relation[0] == keycode:
                return relation[1]

    def tick(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                self.press(self.keycode_to_int(event.key))
            if event.type == pygame.KEYUP:
                self.release(self.keycode_to_int(event.key))


instance = VirtualGamepad()

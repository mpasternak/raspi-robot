
from gamepads.xbox360 import XBox360Controller, init_sdl, process_sdl_events

from boards.nano import NanoBoard

import sys


class XBox360WithNanoRobot(XBox360Controller):
    def __init__(self, board, *args, **kw):
        """

        :ptype board: boards.nano.NanoBoard
        :param args:
        :param kw:
        :return:
        """
        XBox360Controller.__init__(self, *args, **kw)
        self.board = board

    def on_right_stick_moved(self, value_x, value_y):
        self.board.pantilt.set_value(value_x, value_y)

    def on_controller_disconnected(self):
        self.board.reset()

    def on_left_stick_moved(self, value_x, value_y):

        if -0.2 < value_y < 0.2:
            self.board.left_engine.stop()
            self.board.right_engine.stop()

        elif value_y >= 0.2:
            power = value_y
            self.board.right_engine.backward(power)
            self.board.left_engine.backward(power)

        elif value_y < -0.2:
            power = value_y
            self.board.right_engine.forward(abs(power))
            self.board.left_engine.forward(abs(power))


        if value_x >= 0.5:
            power = value_x
            self.board.right_engine.forward(power)
            self.board.left_engine.backward(power)

        elif value_x < -0.5:
            power = abs(value_x)
            self.board.right_engine.backward(power)
            self.board.left_engine.forward(power)



if __name__ == "__main__":
    from logging import log, INFO, basicConfig

    basicConfig(level=INFO, format="[%(asctime)s] %(message)s", datefmt="%Y-%m-%d %H:%M:%S")

    log(INFO, "SDL init")
    init_sdl()

    log(INFO, "Controller INIT")
    port = '/dev/ttyUSB0'
    if sys.platform == 'win32':
        port = 3
    controller = NanoBoard(port)

    log(INFO, "Robot INIT")

    def create_robot(gamepad):
        return XBox360WithNanoRobot(controller, gamepad)

    log(INFO, "mainloop")
    for event in process_sdl_events(create_robot):
        pass
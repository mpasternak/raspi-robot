
# -*- encoding: utf-8 -*-

from pyfirmata import Arduino

class Servo:
    def __init__(self, board, servo_pin_no, neutral_angle=90, min_angle=0, max_angle=180):
        self.servo_pin = board.get_pin("d:%i:s" % servo_pin_no)
        self.neutral_angle = neutral_angle
        self.min_angle = min_angle
        self.max_angle = max_angle

        self.left_range = neutral_angle - min_angle
        self.right_range = max_angle - neutral_angle

    def set_angle(self, value):
        self.servo_pin.write(value)

    def set_value(self, value):
        """

        :param value: float, -1 ... 0 ... +1
        :return:
        """

        if value < 0:
            self.set_angle(self.neutral_angle - self.left_range * abs(value))
            return

        self.set_angle(self.neutral_angle + self.right_range * value)


    def set_neutral(self):
        self.set_angle(self.neutral_angle)


class PanTilt:
    def __init__(self, servo_x, servo_y):
        self.servo_x = servo_x
        self.servo_y = servo_y

    def set_angle(self, angle_x, angle_y):
        self.servo_x.set_angle(angle_x)
        self.servo_y.set_angle(angle_y)

    def set_value(self, value_x, value_y):
        self.servo_x.set_value(value_x)
        self.servo_y.set_value(value_y)

    def reset(self):
        self.servo_x.set_neutral()
        self.servo_y.set_neutral()



class Engine:
    def __init__(self, board, pwm_pin_no, forward_pin_no, backward_pin_no):
        self.pwm_pin = board.get_pin("d:%i:p" % pwm_pin_no)
        self.forward_pin = board.get_pin("d:%i:o" % forward_pin_no)
        self.backward_pin = board.get_pin("d:%i:o" % backward_pin_no)

    def forward(self, power=1.0):
        self.forward_pin.write(1)
        self.backward_pin.write(0)
        self.pwm_pin.write(power)

    def backward(self, power=1.0):
        self.forward_pin.write(0)
        self.backward_pin.write(1)
        self.pwm_pin.write(power)

    def set_power(self, value):
        self.pwm_pin.write(value)

    def stop(self):
        self.forward_pin.write(0)
        self.backward_pin.write(0)
        self.set_power(0)


class Board:
    def __init__(self, 
                 port, 

                 left_engine_pwm_pin=3, 
                 left_engine_forward_pin=4, 
                 left_engine_backward_pin=5,

                 right_engine_pwm_pin=9,
                 right_engine_forward_pin=7,
                 right_engine_backward_pin=8,

                 servo_x_pin=10,
                 servo_x_neutral_angle=70,

                 servo_y_pin=11,
                 servo_y_neutral_angle=150):

        board = Arduino(port)

        self.board = board

        self.left_engine = Engine(
            board, 
            pwm_pin_no=left_engine_pwm_pin, 
            forward_pin_no=left_engine_forward_pin, 
            backward_pin_no=left_engine_backward_pin)

        self.right_engine = Engine(
            board, 
            pwm_pin_no=right_engine_pwm_pin, 
            forward_pin_no=right_engine_forward_pin, 
            backward_pin_no=right_engine_backward_pin)

        servo_x = Servo(
            board, 
            servo_pin_no=servo_x_pin, 
            neutral_angle=servo_x_neutral_angle)

        servo_y = Servo(
            board, 
            servo_pin_no=servo_y_pin, 
            neutral_angle=servo_y_neutral_angle, 
            max_angle=170)

        self.pantilt = PanTilt(servo_x, servo_y)

    def set_camera_servo_x(self, value):
        self.servo_x_pin.write(value)

    def set_camera_servo_y(self, value):
        self.servo_y_pin.write(value)

    def reset(self):
        self.left_engine.stop()
        self.right_engine.stop()
        self.pantilt.reset()


if __name__ == "__main__":
    import time, sys

    port = 3
    if sys.platform == 'linux2':
        port = '/dev/ttyAMA0'
        
    print "Create board"
    controller = Board(port)
    print "Done!"

    print "reset"
    controller.reset()

    for engine in ['right', 'left']:
        for direction in ['backward', 'forward']:
            for value in [0.4, 0.6, 1.0]:
                eng = getattr(controller, "%s_engine" % engine)
                df = getattr(eng, direction)

                print "%s %s power %s for 3 sec" % (engine, direction, value)

                df(value)
                time.sleep(3)

                eng.stop()

    print "reset"
    controller.reset()

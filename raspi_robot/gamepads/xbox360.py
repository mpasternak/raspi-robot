# -*- encoding: utf-8 -*-

import sdl2

class XBox360Controller:

    def __init__(self, sdl_joy_id):
        self.sdl_joy_id = sdl_joy_id
        self.sdl_joy = sdl2.SDL_JoystickOpen(sdl_joy_id)


    def will_handle(self, event):
        if event.type == sdl2.SDL_JOYAXISMOTION:
            if event.jaxis.which == self.sdl_joy_id:
                return True

        elif event.type in [
            sdl2.SDL_JOYBUTTONUP,
            sdl2.SDL_JOYBUTTONDOWN]:
            if event.jbutton.which == self.sdl_joy_id:
                return True

    def on_rb(self, value):
        pass

    def on_lb(self, value):
        pass

    def on_lt(self, value):
        pass

    def on_rt(self, value):
        pass

    def on_left_stick_moved(self, value_x, value_y):
        pass

    def on_left_stick(self, value):
        pass

    def on_right_stick_moved(self, value_x, value_y):
        pass

    def on_right_stick(self, value):
        pass

    def on_dpad_left(self, value):
        pass

    def on_dpad_right(self, value):
        pass

    def on_dpad_up(self, value):
        pass

    def on_dpad_down(self, value):
        pass

    def on_back(self, value):
        pass

    def on_start(self, value):
        pass

    def on_xbox(self, value):
        pass

    def on_a(self, value):
        pass

    def on_b(self, value):
        pass

    def on_x(self, value):
        pass

    def on_y(self, value):
        pass

    BUTTON_TO_FUNCTION_MAP = {
        0: 'on_dpad_up', 
        1: 'on_dpad_down', 
        2: 'on_dpad_left', 
        3: 'on_dpad_right', 

        4: 'on_start', 
        5: 'on_back', 

        6: 'on_right_stick', 
        7: 'on_left_stick', 

        8: 'on_lb', 
        9: 'on_rb', 

        10: 'on_a', 
        11: 'on_b', 

        12: 'on_x', 
        13: 'on_y', 
        
        14: 'on_xbox'

        }

    AXIS_TO_FUNCTION_MAP = {
        0: 'on_left_stick_moved', 
        1: 'on_left_stick_moved', 

        2: 'on_right_stick_moved', 
        3: 'on_right_stick_moved', 

        4: 'on_lt', 
        5: 'on_rt'

    }

    def handle(self, event):
        if event.type in [
            sdl2.SDL_JOYBUTTONUP,
            sdl2.SDL_JOYBUTTONDOWN]:

            function = getattr(self, self.BUTTON_TO_FUNCTION_MAP[event.jbutton.button])
            return function(event.jbutton.state)

        else:

            axis = event.jaxis.axis
            function = getattr(self, self.AXIS_TO_FUNCTION_MAP[axis])

            if axis in [0,1]:
                axes = [0, 1]

            elif axis in [2, 3]:
                axes = [2, 3]

            else:
                # LT or RT
                value = (event.jaxis.value + 32768.0) / 65535.0
                return function(event.jaxis.value)

            args = []
            for axis in axes:
                value = sdl2.SDL_JoystickGetAxis(self.sdl_joy, axis)
                value = value / 32768.0
                args.append(value)

            #print "CALL", function, args
            return function(*args)

        raise Exception("I should not be here")

def init_sdl():
    import sdl2, sdl2.ext
    sdl2.SDL_Init(sdl2.SDL_INIT_JOYSTICK)

def process_sdl_events():
    import sdl2
    while True:
        event = sdl2.SDL_Event()
        sdl2.SDL_WaitEvent(event)
        yield event

if __name__ == "__main__":
    init_sdl()

    xbox360controller = XBox360Controller(0)

    for event in process_sdl_events():
        if xbox360controller.will_handle(event):
            xbox360controller.handle(event)

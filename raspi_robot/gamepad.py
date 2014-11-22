# -*- encoding: utf-8 -*-

import sdl2
import logging
from sdl2 import gamecontroller

DEBUG = False


class GamepadController:

    def __init__(self, sdl_controller_id):
        self.sdl_controller_id = sdl_controller_id
        self.sdl_controller = sdl2.SDL_GameControllerOpen(sdl_controller_id)

        self.sdl_joy = sdl2.SDL_GameControllerGetJoystick(self.sdl_controller)
        self.sdl_joy_id = sdl2.SDL_JoystickInstanceID(self.sdl_joy)
        
        guid = sdl2.SDL_JoystickGetDeviceGUID(self.sdl_joy_id)
        logging.log(logging.INFO, "Joystick GUID: %s " % guid)
        logging.log(logging.INFO, "Mapping: %s" % sdl2.SDL_GameControllerMappingForGUID(guid))

    def close(self):
        sdl2.SDL_GameControllerClose(self.sdl_controller)
        self.on_controller_disconnected()

    def on_controller_disconnected(self):
        pass

    def will_handle(self, event):
        if event.type in [
        	sdl2.SDL_CONTROLLERBUTTONDOWN,
                sdl2.SDL_CONTROLLERBUTTONUP,
                ]:

            if event.cbutton.which == self.sdl_joy_id:
                return True

        if event.type in [
        	sdl2.SDL_CONTROLLERAXISMOTION, 
                ]:
            if event.caxis.which == self.sdl_joy_id:
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
        'dpup': 'on_dpad_up',
        'dpdown': 'on_dpad_down',
        'dpleft': 'on_dpad_left',
        'dpright': 'on_dpad_right',

        'start': 'on_start',
        'back': 'on_back',

        
        'rightstick': 'on_right_stick',
        'leftstick': 'on_left_stick',

        'leftshoulder': 'on_lb',
        'rightshoulder': 'on_rb',

        'a': 'on_a',
        'b': 'on_b',
        'x': 'on_x',
        'y': 'on_y',
        
        'guide': 'on_xbox'

        }

    AXIS_TO_FUNCTION_MAP = {
        'leftx': 'on_left_stick_moved',
        'lefty': 'on_left_stick_moved',

        'rightx': 'on_right_stick_moved',
        'righty': 'on_right_stick_moved',

        'lefttrigger': 'on_lt',
        'righttrigger': 'on_rt'

    }

    def handle(self, event):
        
        if event.type in [
        	sdl2.SDL_CONTROLLERBUTTONDOWN ,
            	sdl2.SDL_CONTROLLERBUTTONUP]:
                    
            button = event.cbutton.button
            state = event.cbutton.state
            
            buttonName = sdl2.SDL_GameControllerGetStringForButton(button)
            function = getattr(self, self.BUTTON_TO_FUNCTION_MAP[buttonName])
            if DEBUG: print "CALLING", function, state
            return function(state)

        elif event.type in [sdl2.SDL_CONTROLLERAXISMOTION]:

            axis = event.caxis.axis
            axisName = sdl2.SDL_GameControllerGetStringForAxis(axis)
            function = getattr(self, self.AXIS_TO_FUNCTION_MAP[axisName])

            if axisName in ['leftx', 'lefty']:
                axes = ['leftx', 'lefty']

            elif axisName in ['rightx', 'righty']:
                axes = ['rightx', 'righty']

            else:
                # LT or RT
                value = (event.caxis.value + 32768.0) / 65535.0
                if DEBUG: print "CALL", function, value
                return function(value)

            args = []
            for axis in axes:
                value = sdl2.SDL_GameControllerGetAxis(self.sdl_controller,
                	sdl2.SDL_GameControllerGetAxisFromString(axis))
                value = value / 32768.0
                args.append(value)

            if DEBUG: print "CALL", function, args
            return function(*args)

        raise Exception("I should not be here")

def init_sdl():
    logging.log(logging.INFO, "sdl init...")
    import sdl2, sdl2.ext
    sdl2.SDL_Init(sdl2.SDL_INIT_GAMECONTROLLER)
    sdl2.SDL_GameControllerAddMappingsFromRW(sdl2.SDL_RWFromFile("gamecontrollerdb.txt", "rb"), 1)


def process_sdl_events(controller_class):
    import sdl2

    controllers = []

    while True:
        event = sdl2.SDL_Event()
        sdl2.SDL_WaitEvent(event)

        if event.type == sdl2.SDL_CONTROLLERDEVICEADDED:
            logging.log(logging.INFO, "adding controller")
            c = controller_class(event.cdevice.which)
            controllers.append(c)
            pass

        elif event.type == sdl2.SDL_CONTROLLERDEVICEREMOVED:
            remove = []

            for elem in controllers:
                if elem.sdl_controller_id == event.cdevice.which:
                    elem.close()
                    remove.append(elem)

            for elem in remove:
                controllers.remove(elem)

            pass
        else:
            handled = False
            if DEBUG: print "Event type %s passing to controller..." % event.type
            for controller in controllers:
                if DEBUG: print "Checking if ", controller, "will handle...",
                if controller.will_handle(event):
                    if DEBUG: print "yes!"
                    handled = True
                    controller.handle(event)
                    break
                else:
                    if DEBUG: print "-no"

            if not handled:
                yield event

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    init_sdl()

    global DEBUG
    DEBUG = True

    for event in process_sdl_events(controller_class=GamepadController):
        pass

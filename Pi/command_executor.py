import shared

from threading import Event

from hardware import Motors, Lights, Distance

class CommandExecutor(object):    

    __instance = None
    
    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = object.__new__(cls)
            cls.__instance.__initialized = False
        return cls.__instance

    def __init__(self):
        if(self.__initialized): return
        
        self.__initialized = True
        
        self.distance = Distance()
        
        self.motors = Motors()
        
        self.lights = Lights()    

        self.distance_ev = Event()
        
        self.command_dict = {
            'forward': self.motors.go_forward,
            'backward': self.motors.go_backward,
            'left': self.motors.turn_left,
            'right': self.motors.turn_right,
            'stop': self.motors.stop,
            'lights_on': self.lights.lights_on,
            'lights_off': self.lights.lights_off,
            'distance_on': self.distance.distance_on,
            'distance_off': self.distance.distance_off,
            'stop_stream': shared.camera.stop_recording
        }
        
    def interpret(self, command):
        if command in self.command_dict:
            self.command_dict[command]()
            result = command
        elif command == 'start_stream':
            shared.camera.start_recording(shared.output, format = 'mjpeg')
            result = command
        elif command == 'get_distance':
            result = self.distance.get_distance()    
        else:
            result = command        
        return result

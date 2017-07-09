import shared
import time

class Distance(object):
    DISTANCE_ON = '2'
    GET_DISTANCE = '3'
    DISTANCE_OFF = '4'
    
    __instance = None
    
    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = object.__new__(cls)
            cls.__instance.__initialized = False
        return cls.__instance
    
    def __init__(self):
        if(self.__initialized): return        
        self.__initialized = True        
        self.distance = "..."
    
    def distance_on(self):
        shared.comm.send(Distance.DISTANCE_ON)
    
    def get_distance(self):
        shared.comm.send(Distance.GET_DISTANCE)
        shared.command_executor.distance_ev.wait()
        return self.distance
    
    def distance_off(self):
        shared.comm.send(Distance.DISTANCE_OFF)
        
class Motors(object):
    SET_MOTORS = '5'

    __instance = None
    
    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = object.__new__(cls)
            cls.__instance.__initialized = False
        return cls.__instance
    
    def __init__(self):
        if(self.__initialized): return        
        self.__initialized = True
        self.going_forward = False

    def set_motor_powers(self, left_power, right_power):
        if left_power < -100 or left_power > 100 or right_power < -100 or right_power > 100:
            raise ValueError('Bad motor power range: ' + str(left_power)+' '+str(right_power))
        shared.comm.send(Motors.SET_MOTORS+';'+str(left_power)+','+str(right_power))
        print('Sent: ' + Motors.SET_MOTORS+';'+str(left_power)+','+str(right_power))
 
    def go(self, left_power, right_power, stop = False, duration = 1):
        self.set_motor_powers(left_power, right_power)
        if stop:
            time.sleep(duration)
            self.set_motor_powers(0, 0)

    def stop(self):
        self.set_motor_powers(0, 0)
        self.going_forward = False

    def go_forward(self):
        self.going_forward = True
        self.go(70, 70)
        
    def go_backward(self):
        self.go(-60, -60)
	
    def turn_left(self):
        self.go(-60, 60)

    def turn_right(self):
        self.go(60, -60)

        
class Lights(object):
    LIGHTS_ON = '6'
    LIGHTS_OFF = '7'
	
    __instance = None
    
    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = object.__new__(cls)
        return cls.__instance
    
    def lights_on(self):
        shared.comm.send(Lights.LIGHTS_ON)
        
    def lights_off(self):
        shared.comm.send(Lights.LIGHTS_OFF)
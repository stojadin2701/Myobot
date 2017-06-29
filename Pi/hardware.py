import shared
import time

class Distance(object):
    COMMAND = '2'
	
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
    
    def request_distance(self):
        shared.comm.send(Distance.COMMAND)
        shared.command_executor.distance_ev.wait()
        return self.distance
        

class Motors(object):
    COMMAND = '3'

    __instance = None
    
    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = object.__new__(cls)
        return cls.__instance
    
    def set_motor_powers(self, left_power, right_power):
        if left_power < -100 or left_power > 100 or right_power < -100 or right_power > 100:
            raise ValueError('Bad motor power range: ' + str(left_power)+' '+str(right_power))
        shared.comm.send(Motors.COMMAND+';'+str(left_power)+','+str(right_power))
        print('Sent: ' + Motors.COMMAND+';'+str(left_power)+','+str(right_power))
        #shared.comm.send(str(left_power))
        #print(shared.comm.receive())
        #shared.comm.send(str(right_power))
        #print(shared.comm.receive())
			
    def go(self, left_power, right_power, stop = False, duration = 1):
        self.set_motor_powers(left_power, right_power)
        if stop:
            time.sleep(duration)
            self.set_motor_powers(0, 0)
   
    def stop(self):
        self.set_motor_powers(0, 0)
        #with shared.lock:
        shared.going_forward = False

    def go_forward(self):
        #with shared.lock:
        shared.going_forward = True
        self.go(70, 70)
        
    def go_backward(self):
        self.go(-60, -60)
	
    def turn_left(self):
        self.go(-60, 60)

    def turn_right(self):
        self.go(60, -60)

        
class Lights(object):
    LIGHTS_ON = '4'
    LIGHTS_OFF = '5'
	
    __instance = None
    
    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = object.__new__(cls)
        return cls.__instance
    
    def on(self):
        shared.comm.send(Lights.LIGHTS_ON)
        
    def off(self):
        shared.comm.send(Lights.LIGHTS_OFF)
import time

import shared

class Motors(object):
    COMMAND = '2'

    @staticmethod
    def set_motor_powers(left_power, right_power):
        if left_power < -100 or left_power > 100 or right_power < -100 or right_power > 100:
            raise ValueError('Bad motor power range: ' + str(left_power)+' '+str(right_power))
        shared.comm.send(Motors.COMMAND+';'+str(left_power)+','+str(right_power))
        print('Sent: ' + Motors.COMMAND+';'+str(left_power)+','+str(right_power))
        #shared.comm.send(str(left_power))
        #print(shared.comm.receive())
        #shared.comm.send(str(right_power))
        #print(shared.comm.receive())
			
    @staticmethod
    def go(left_power, right_power, stop = False, duration = 1):
        Motors.set_motor_powers(left_power, right_power)
        if stop:
            time.sleep(duration)
            Motors.set_motor_powers(0, 0)
   
    @staticmethod
    def stop():
        Motors.set_motor_powers(0, 0)
        #with shared.lock:
        shared.going_forward = False

    @staticmethod
    def go_forward():
        #with shared.lock:
        shared.going_forward = True
        Motors.go(70, 70)
        
    @staticmethod
    def go_backward():
        Motors.go(-60, -60)
	
    @staticmethod
    def turn_left():
        Motors.go(-60, 60)

    @staticmethod
    def turn_right():
        Motors.go(60, -60)

import time

import shared

class Motors(object):
    COMMAND = '2'

    @staticmethod
    def set_motor_powers(left_power, right_power):
        if left_power < -100 or left_power > 100 or right_power < -100 or right_power > 100:
            raise ValueError('Bad motor power range: ' + str(left_power)+' '+str(right_power))
        #with shared.comm_lock:
        #shared.comm.send()
        shared.comm.send(Motors.COMMAND)
        shared.comm.send(str(left_power))
        #print(shared.comm.receive())
        shared.comm.send(str(right_power))
        #print(shared.comm.receive())
			
    @staticmethod
    def go(left_power, right_power, stop = False, duration = 1):
        Motors.set_motor_powers(left_power, right_power)
        if stop:
            time.sleep(duration)
            Motors.set_motor_powers(0, 0)

    @staticmethod
    def stop():
        #with shared.lock:
        shared.going_forward = False
        Motors.set_motor_powers(0, 0)

    @staticmethod
    def stop_forever():
        Motors.set_motor_powers(0, 0)
        #with shared.lock:
        shared.going_forward = False
		
    @staticmethod
    def go_forward(duration):
        #with shared.lock:
        shared.going_forward = True
        Motors.go(60, 60, True, duration)
        #with shared.lock:
        shared.going_forward = False

    @staticmethod
    def go_backward(duration):
        Motors.go(-70, -70, True, duration)
	
    @staticmethod
    def turn_left(duration):
        Motors.go(-80, 80, True, duration)

    @staticmethod
    def turn_right(duration):
        Motors.go(80, -80, True, duration)


    @staticmethod
    def go_forward_forever():
        #with shared.lock:
        shared.going_forward = True
        Motors.go(50, 50)
        
    @staticmethod
    def go_backward_forever():
        Motors.go(-60, -60)
	
    @staticmethod
    def turn_left_forever():
        Motors.go(-60, 60)

    @staticmethod
    def turn_right_forever():
        Motors.go(60, -60)

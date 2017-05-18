import time

import shared

class Motors(object):
	COMMAND = 2

	@staticmethod
	def set_motor_powers(left_power, right_power):
		if left_power < -100 or left_power > 100 or right_power < -100 or right_power > 100:
			raise ValueError('Bad motor power range: ' + str(left_power)+' '+str(right_power))
		with shared.lock:			
			shared.comm.send(Motors.COMMAND)
			shared.comm.send(left_power+100)	#move range in order to send only positive numbers
			shared.comm.send(right_power+100)
			
	@staticmethod
	def go(left_power, right_power, duration):
		Motors.set_motor_powers(left_power, right_power)
		time.sleep(duration)
		Motors.set_motor_powers(0, 0)

	@staticmethod
	def stop():
		Motors.set_motor_powers(0, 0)
			
	
	@staticmethod
	def go_forward(duration):
		with shared.lock:
			shared.going_forward = True
		Motors.go(60, 60, duration)
		with shared.lock:
			shared.going_forward = False

	@staticmethod
	def go_backward(duration):
		Motors.go(-70, -70, duration)
	
	@staticmethod
	def turn_left(duration):
		Motors.go(-80, 80, duration)

	@staticmethod
	def turn_right(duration):
		Motors.go(80, -80, duration)
	

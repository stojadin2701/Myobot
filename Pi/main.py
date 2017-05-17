import serial
import time
import threading

START = 0

ser = serial.Serial('/dev/ttyACM0', 9600)

counter = 0

lock = threading.RLock()
going_forward = False


class CommProtocol(object):
	@staticmethod
	def send(data):
		ser.write(str(chr(data)))
	
	@staticmethod
	def receive():
		return ser.readline()

class DistanceSensor(threading.Thread):
	COMMAND = 1
	DISTANCE_THRESHOLD = 20
	
	def run(self):
		while True:
			with lock:
				CommProtocol.send(DistanceSensor.COMMAND)
				distance = CommProtocol.receive()
				print(distance)
				global going_forward
				if int(distance) < DistanceSensor.DISTANCE_THRESHOLD and going_forward:
					going_forward = False
					print("Obstacle detected\n")
					Motors.stop()				
					break
			time.sleep(.035)
		return


class Motors(object):
	COMMAND = 2

	@staticmethod
	def set_motor_powers(left_power, right_power):
		if left_power < -100 or left_power > 100 or right_power < -100 or right_power > 100:
			raise ValueError('Bad motor power range: ' + str(left_power)+' '+str(right_power))
		with lock:			
			CommProtocol.send(Motors.COMMAND)
			CommProtocol.send(left_power+100)	#move range in order to send only positive numbers
			CommProtocol.send(right_power+100)
			
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
		global going_forward
		with lock:
			going_forward = True
		Motors.go(60, 60, duration)
		with lock:
			going_forward = False

	@staticmethod
	def go_backward(duration):
		Motors.go(-70, -70, duration)
	
	@staticmethod
	def turn_left(duration):
		Motors.go(-80, 80, duration)

	@staticmethod
	def turn_right(duration):
		Motors.go(80, -80, duration)
		



distance_thread = DistanceSensor()

time.sleep(2)

CommProtocol.send(START)

print(CommProtocol.receive())

distance_thread.start()

try:
	Motors.go_forward(1);
#	Motors.go_backward(1);
#	Motors.turn_left(1);
#	Motors.turn_right(1);	

	"""
	print(CommProtocol.receive())
	print(CommProtocol.receive())
	print(CommProtocol.receive())
	print(CommProtocol.receive())
	print(CommProtocol.receive())
	print(CommProtocol.receive())
	print(CommProtocol.receive())
	print(CommProtocol.receive())
	"""



except Exception as err:
	print (err)


distance_thread.join()


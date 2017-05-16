import serial
import time
import threading


START = 0

ser = serial.Serial('/dev/ttyACM0', 9600)

counter = 0

def send_command(command):
	ser.write(str(chr(command)))
	return;

def receive_data():
	return ser.readline()

class DistanceSensor(threading.Thread):
	COMMAND = 1
	DISTANCE_THRESHOLD = 20
	
	def run(self):
		while True:
			send_command(DistanceSensor.COMMAND)
			distance = receive_data()
			print(distance+'\n')
			#print("Distance is "+ distance + "Distance threshold is " + DistanceSensor.DISTANCE_THRESHOLD+"\n")
			if int(distance) < DistanceSensor.DISTANCE_THRESHOLD:
				print("WARNING!!!")
				break
			time.sleep(.035)
		return


class Motors(object):
	COMMAND = 1 

distance_thread = DistanceSensor()

send_command(START)
receive_data()
#receive_data()

distance_thread.start()

distance_thread.join()

"""
while True:
	counter+=1
	ser.write(str(chr(counter)))
	print ser.readline()
	time.sleep(1)
	if(counter == 3):
		counter=0
"""

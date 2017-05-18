import time
import threading

import shared

from distance_sensor import DistanceSensor
from motors import Motors
from getch import _Getch

shared.init()

distance_thread = DistanceSensor()

time.sleep(2)

START_COMMAND = 0
shared.comm.send(START_COMMAND)

print(shared.comm.receive())

try:
	distance_thread.start()

	getch = _Getch()

	while True:
		direction = getch.impl()
		print(direction)
		if(direction == 'w'):
			Motors.go_forward(1)
		elif(direction == 's'):
			Motors.go_backward(1)
		elif(direction == 'a'):
			Motors.turn_left(1)
		elif(direction == 'd'):
			Motors.turn_right(1)	
		else:
			break

except Exception as err:
	print (err)

finally:
	distance_thread.join()

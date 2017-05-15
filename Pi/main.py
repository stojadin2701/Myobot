import serial
import time

ser = serial.Serial('/dev/ttyACM0', 9600)

counter = 32

while True:
	counter+=1
	ser.write(str(chr(counter)))
	print ser.readline()
	time.sleep(.1)
	if(counter == 255):
		counter=32


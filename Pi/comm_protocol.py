import serial

class Communicator(object):
	#SER = serial.Serial('/dev/ttyACM0', 9600)

	def __init__(self, port, baud_rate):
		self.ser = serial.Serial(port, baud_rate)

	def send(self, data):
		self.ser.write(str(chr(data)))
	
	def receive(self):
		return self.ser.readline()



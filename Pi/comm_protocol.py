import serial

class Communicator(object):
    def __init__(self, port, baud_rate):
        self.ser = serial.Serial(port, baud_rate)

    def send(self, data):
        self.ser.write(bytes(str(chr(data)),'UTF-8'))
	
    def receive(self):
        return self.ser.readline().decode('UTF-8')

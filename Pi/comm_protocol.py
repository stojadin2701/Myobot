import serial

class Communicator(object):
    def __init__(self, port, baud_rate):
        self.ser = serial.Serial(port, baud_rate)

    def send(self, data):
        self.ser.write(bytes(data+'\n', 'utf-8'))
        #print('sending: '+data)
        
	
    def receive(self):
        return self.ser.readline().decode('utf-8')

    def send_int(self, data):
        self.ser.write(bytes(str(chr(data)), 'utf-8'))
        #print('sending: '+str(data))


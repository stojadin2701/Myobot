import serial

from threading import Lock

class Communicator(object):
    def __init__(self, port, baud_rate):
        self.ser = serial.Serial(port, baud_rate)
        self.comm_lock = Lock()

    def send(self, data):
        with self.comm_lock:
            self.ser.write(bytes(data+'\n', 'utf-8'))
        #print('sending: '+data)
        
	
    def receive(self):
        return self.ser.readline().decode('utf-8')

    def send_int(self, data):
        with self.comm_lock:
            self.ser.write(bytes(str(chr(data)), 'utf-8'))
        #print('sending: '+str(data))


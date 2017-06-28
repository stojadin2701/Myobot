import serial

from threading import Lock

class Communicator(object):
    def __init__(self, port, baud_rate):
        self.ser = serial.Serial(port, baud_rate)
        self.comm_lock = Lock()

    def send(self, data):
        with self.comm_lock:
            self.ser.write(bytes(data+'\n', 'utf-8'))
            #print('out' + str(self.ser.out_waiting))
        #print('sending: '+data)
        
	
    def receive(self):
        print('in:' + str(self.ser.inWaiting()))
        return self.ser.readline().decode('utf-8')


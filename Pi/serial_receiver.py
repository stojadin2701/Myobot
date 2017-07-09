import time
import threading

import shared

class SerialReceiver(threading.Thread):
    
    def __init__(self, receiver_ev):
        super(SerialReceiver, self).__init__()
        self.receiver_ev = receiver_ev

    def run(self):
        while self.receiver_ev.is_set():
            rcv=shared.comm.receive()            
            if rcv[0] == '&':
                shared.command_executor.distance.distance = rcv[1:len(rcv)]
                shared.command_executor.distance_ev.set()
                shared.command_executor.distance_ev.clear()
                print("Distance: " + shared.command_executor.distance.distance)
            else:
                print(rcv)
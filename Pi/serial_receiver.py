import time
import threading

import shared

class SerialReceiver(threading.Thread):
    
    def __init__(self, receiver_ev):
        super(SerialReceiver, self).__init__()
        self.receiver_ev = receiver_ev
        self.distance = '---'

    def get_last_distance(self):
        #maybe some mutex here
        return self.distance

    def run(self):
        while self.receiver_ev.is_set():
            #with shared.comm_lock:
            #decode messages based on the received value
            #self.distance = shared.comm.receive()
            #print(self.distance)
            
            rcv=shared.comm.receive()            
            if rcv[0] == '&':
                self.distance = rcv[1:len(rcv)]
                print("Distance: " + self.distance)
            else:
                print(rcv)
                """
            if rcv[0]=="/" :
                print ("Message: ",rcv[1:len(rcv)-1])
                continue
            elif rcv[0]=="<" :
                print ("Left motor power: ",rcv[1:len(rcv)-1])
            elif rcv[0]==">" :
                print ("Right motor power: ",rcv[1:len(rcv)-1])
            else :
                print ("Distance: ",rcv)
                continue
            """

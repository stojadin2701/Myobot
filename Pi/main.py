import io
import time
import threading

import shared

from heartbeat import Heartbeat
from serial_receiver import SerialReceiver
from server import StreamingServer
from server import StreamingHandler
from threading import Event

def main():    
    shared.init()
    
    receiver_ev = Event()
    receiver_ev.set()
    receiver_thread = SerialReceiver(receiver_ev)   
    
    heartbeat_ev = Event()
    heartbeat_ev.set()
    heartbeat_thread = Heartbeat(heartbeat_ev)
    
    time.sleep(2)    
    
    START = '1'
    shared.comm.send(START)
    rcv=shared.comm.receive()
    print(rcv)
       
    with shared.camera:
        try:
            receiver_thread.start()
            heartbeat_thread.start()
            
            server = StreamingServer(shared.address, StreamingHandler)
            print('Server started on port ' + str(shared.address[1]))
            server.serve_forever()
        except Exception as err:
            print(err)
        finally:           
            heartbeat_ev.clear()
            heartbeat_thread.join()
            END = '9'
            shared.comm.send(END)
            receiver_ev.clear()            
            receiver_thread.join()      
            
if __name__ == '__main__':
    main()
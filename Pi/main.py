import io
import time
import threading

import shared

from motors import Motors
from getch import _Getch
from server import StreamingServer
from server import StreamingHandler

def main():    
    shared.init()
    
    time.sleep(2)
       
    with shared.camera:
        try:
            shared.receiver_thread.start()
            shared.heartbeat_thread.start()
            
            START_COMMAND = '1'
            shared.comm.send(START_COMMAND)
            server = StreamingServer(shared.address, StreamingHandler)
            print('Server started on port ' + str(shared.address[1]))
            server.serve_forever()
        except Exception as err:
            print(err)
        finally:
            shared.receiver_ev.clear()
            shared.heartbeat_ev.clear()
            shared.receiver_thread.join()
            shared.heartbeat_thread.join()

if __name__ == '__main__':
    main()


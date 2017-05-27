import io
import time
import threading

import shared

from distance_sensor import DistanceSensor
from motors import Motors
from getch import _Getch
from server import StreamingServer
from server import StreamingHandler

def main():
    shared.init()

    time.sleep(2)

    START_COMMAND = 0
    shared.comm.send(START_COMMAND)

    print(shared.comm.receive())

    with shared.camera:
        try:
#            shared.distance_thread.start()
            server = StreamingServer(shared.address, StreamingHandler)
            server.serve_forever()
        except Exception as err:
            print(err)
        finally:
            shared.distance_ev.clear()
#            shared.distance_thread.join()

if __name__ == '__main__':
    main()

    """
    getch = _Getch()

    while True:
        direction = getch.impl()
        print(direction)
        if(direction == 'w'):
            Motors.go_forward(1)
        elif(direction == 's'):
            Motors.go_backward(1)
        elif(direction == 'a'):
            Motors.turn_left(1)
        elif(direction == 'd'):
            Motors.turn_right(1)	
        else:
            break
    """

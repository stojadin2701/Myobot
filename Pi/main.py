import io
import time
import threading

import shared

from distance_sensor import DistanceSensor
from motors import Motors
from getch import _Getch
from server import StreamingServer
from server import StreamingOutput
from server import StreamingHandler

shared.init()

distance_thread = DistanceSensor()

time.sleep(2)

START_COMMAND = 0
shared.comm.send(START_COMMAND)

print(shared.comm.receive())

try:
#    distance_thread.start()
    
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

    with shared.camera:
        shared.output = StreamingOutput()
        try:
                address = ('', 8080)
                server = StreamingServer(address, StreamingHandler)
                server.serve_forever()
        except Exception as err:
            print(err)

except Exception as err:
    print (err)

#finally:
 #   distance_thread.join()

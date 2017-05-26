import time
import threading

import shared

from motors import Motors

class DistanceSensor(threading.Thread):
    COMMAND = 1
    DISTANCE_THRESHOLD = 20

    def run(self):
        while True:
            with shared.lock:
                shared.comm.send(DistanceSensor.COMMAND)
                distance = shared.comm.receive()
                print(distance)
                if int(distance) < DistanceSensor.DISTANCE_THRESHOLD and shared.going_forward:
                    shared.going_forward = False
                    print("Obstacle detected\n")
                    Motors.stop()				
                    break
            time.sleep(.035)	



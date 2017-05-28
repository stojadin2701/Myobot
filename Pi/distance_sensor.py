import time
import threading

import shared

from motors import Motors

class DistanceSensor(threading.Thread):
    COMMAND = 1
    DISTANCE_THRESHOLD = 20

    def __init__(self, distance_ev):
        super(DistanceSensor, self).__init__()
        self.distance_ev = distance_ev
        self.distance = '---'

    def get_last_distance(self):
        #ovde mozda neko iskljucivanje
        return self.distance

    def run(self):
        while self.distance_ev.is_set():
            with shared.comm_lock:
                shared.comm.send(DistanceSensor.COMMAND)
                self.distance = shared.comm.receive()
            print(self.distance)
            if int(self.distance) < DistanceSensor.DISTANCE_THRESHOLD and shared.going_forward:
                shared.going_forward = False
                print("Obstacle detected\n")
                Motors.stop()	
                break
            time.sleep(.035)

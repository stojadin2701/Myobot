import time
import threading

import shared

class SerialReceiver(threading.Thread):
    
    def __init__(self, heartbeat_ev):
        super(SerialReceiver, self).__init__()
        self.heartbeat_ev = heartbeat_ev
        self.distance = '---'

    def run(self):
        while self.heartbeat_ev.is_set():
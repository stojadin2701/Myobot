import time
import threading

import shared

class Heartbeat(threading.Thread):
    COMMAND = '3'
    
    def __init__(self, heartbeat_ev):
        super(Heartbeat, self).__init__()
        self.heartbeat_ev = heartbeat_ev

    def run(self):
        while self.heartbeat_ev.is_set():
            shared.comm.send(Heartbeat.COMMAND)
            time.sleep(0.7)
import io
import threading
from comm_protocol import Communicator


def init():
    global lock
    global going_forward
    global comm
    
    global index
    global myo
    global myscript

    global output

    lock = threading.RLock()
    going_forward = False
    comm = Communicator('/dev/ttyACM0', 9600)
      
    with io.open('web/index.html', 'r') as f:
        index = f.read()
    with io.open('web/myo.js', 'r') as f:
        myo = f.read()
    with io.open('web/myscript.js', 'r') as f:
        myscript = f.read()

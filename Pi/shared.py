import threading
from comm_protocol import Communicator


def init():
	global lock
	global going_forward
	global comm
	lock = threading.RLock()
	going_forward = False
	comm = Communicator('/dev/ttyACM0', 9600)



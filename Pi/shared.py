import io
import sys

from threading import Lock
from threading import Event
from configparser import ConfigParser
from picamera import PiCamera
from string import Template

from comm_protocol import Communicator
from server import StreamingOutput
#from distance_sensor import DistanceSensor
from serial_receiver import SerialReceiver

def init():
    #global motor_lock
    global comm_lock

    global going_forward
    global comm
    
    global index
    global myo
    global myscript

    global output

    global address

    global camera

    global config

    #global distance_ev
    
    #global distance_thread

    global receiver_ev

    global receiver_thread
    
    config = ConfigParser()
    config.read('config.ini')

    #motor_lock = Lock()
    comm_lock = Lock()
    going_forward = False

    try:
        comm = Communicator(config.get('arduino', 'port'), config.getint('arduino', 'baud_rate'))
    except:
        sys.exit('Could not find Arduino on ' + config.get('arduino', 'port'))

    with io.open(config.get('web', 'index_location'), 'r') as f:
        index = Template(f.read()).safe_substitute(dict(img_width=config.get('web', 'img_width'), img_height=config.get('web', 'img_height')))

    with io.open(config.get('web', 'myo_location'), 'r') as f:
        myo = f.read()
    with io.open(config.get('web', 'myscript_location'), 'r') as f:
        myscript = f.read()

    output = StreamingOutput()

    address = ('', config.getint('web', 'port'))
  
    camera = PiCamera(resolution = config.get('camera', 'resolution'), framerate = config.getint('camera', 'framerate'))
    camera.hflip = config.getboolean('camera', 'hflip')
    camera.vflip = config.getboolean('camera', 'vflip')
    
    #distance_ev = Event()
    #distance_ev.set()
    #distance_thread = DistanceSensor(distance_ev)
    receiver_ev = Event()
    receiver_ev.set()
    receiver_thread = SerialReceiver(receiver_ev)

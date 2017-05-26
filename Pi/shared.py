import io

from threading import RLock
from configparser import ConfigParser
from picamera import PiCamera
from string import Template

from comm_protocol import Communicator
from server import StreamingOutput

def init():
    global lock
    global going_forward
    global comm
    
    global index
    global myo
    global myscript

    global output

    global address

    global camera

    global config
    
    config = ConfigParser()
    config.read('config.ini')

    lock = RLock()
    going_forward = False
    comm = Communicator(config.get('arduino', 'port'), config.getint('arduino', 'baud_rate'))
      
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

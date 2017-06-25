import io
import sys

from threading import Lock
from threading import Event
from configparser import ConfigParser
from picamera import PiCamera
from string import Template

from comm_protocol import Communicator
from server import StreamingOutput
from serial_receiver import SerialReceiver
from heartbeat import Heartbeat

def init():
    global comm_lock

    global going_forward
    
    global comm
    
    global output

    global address

    global camera

    global config

    global receiver_ev

    global receiver_thread
    
    global heartbeat_ev

    global heartbeat_thread

    global web_file_mappings
    
    config = ConfigParser()
    config.read('config.ini')

    comm_lock = Lock()
    going_forward = False

    try:
        comm = Communicator(config.get('arduino', 'port'), config.getint('arduino', 'baud_rate'))
    except:
        sys.exit('Could not find Arduino on ' + config.get('arduino', 'port'))

    web_file_mappings = {}

    #read files
    for page in config.options('web_path_mappings'):
        with io.open(config.get('web_path_mappings', page), 'r') as f:
            web_file_mappings[config.get('web_path_mappings', page)[6:]] = f.read() #removes ../Web from the path
        #print("x %s:::%s" % (path, config.get('web_path_mappings', path)))

    #apply templates
    Template(web_file_mappings['/index.html']).safe_substitute(dict(img_width=config.get('web_params', 'img_width'), img_height=config.get('web_params', 'img_height')))

    #encode
    for p, f in web_file_mappings.items():
        web_file_mappings[p] = f.encode('utf-8')
    
    output = StreamingOutput()

    address = ('', config.getint('web_params', 'port'))
  
    camera = PiCamera(resolution = config.get('camera', 'resolution'), framerate = config.getint('camera', 'framerate'))
    camera.hflip = config.getboolean('camera', 'hflip')
    camera.vflip = config.getboolean('camera', 'vflip')
    
    receiver_ev = Event()
    receiver_ev.set()
    receiver_thread = SerialReceiver(receiver_ev)   
    
    heartbeat_ev = Event()
    heartbeat_ev.set()
    heartbeat_thread = Heartbeat(heartbeat_ev)

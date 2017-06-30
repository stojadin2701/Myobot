import io
import sys

from configparser import ConfigParser
from picamera import PiCamera

from threading import Event
from comm_protocol import Communicator
from server import StreamingOutput
from command_executor import CommandExecutor

def init():    
    global comm
    
    global output

    global address

    global camera

    global config    

    global web_file_mappings
    
    global command_executor
    
    global distance_ev
    
    config = ConfigParser()
    config.read('config.ini')

    try:
        comm = Communicator(config.get('arduino', 'port'), config.getint('arduino', 'baud_rate'))
    except:
        sys.exit('Could not find Arduino on ' + config.get('arduino', 'port'))
  
    output = StreamingOutput()

    address = ('', config.getint('web_params', 'port'))
  
    camera = PiCamera(resolution = config.get('camera', 'resolution'), framerate = config.getint('camera', 'framerate'))
    camera.hflip = config.getboolean('camera', 'hflip')
    camera.vflip = config.getboolean('camera', 'vflip')   
    
    distance_ev = Event()
    
    command_executor = CommandExecutor()

import io
import logging
import socketserver

import shared

from threading import Condition
from http import server

from command_executor import CommandExecutor

"""

FINGERS_SPREAD='1'
WAVE_IN='2'
WAVE_OUT='3'
FIST='4'
DOUBLE_TAP='5'

FINGERS_SPREAD_OFF='6'
WAVE_IN_OFF='7'
WAVE_OUT_OFF='8'
FIST_OFF='9'
DOUBLE_TAP_OFF='10'




command_dict = {
        FINGERS_SPREAD: Motors.go_forward_forever,
        WAVE_IN: Motors.turn_left_forever,
        WAVE_OUT: Motors.turn_right_forever,
        FIST: Motors.go_backward_forever,
        DOUBLE_TAP: Motors.stop_forever,
        FINGERS_SPREAD_OFF: Motors.stop_forever,
        WAVE_IN_OFF: Motors.stop_forever,
        WAVE_OUT_OFF: Motors.stop_forever,
        FIST_OFF: Motors.stop_forever,
        DOUBLE_TAP_OFF: Motors.stop_forever
}

"""

class StreamingOutput(object):
        def __init__(self):
                self.frame = None
                self.buffer = io.BytesIO()
                self.condition = Condition()

        def write(self, buf):
                if buf.startswith(b'\xff\xd8'):
                        # New frame, copy the existing buffer's content and notify all
                        # clients it's available
                        self.buffer.truncate()
                        with self.condition:
                                self.frame = self.buffer.getvalue()
                                self.condition.notify_all()
                        self.buffer.seek(0)
                return self.buffer.write(buf)

class StreamingHandler(server.BaseHTTPRequestHandler):
         def do_POST(self):
                length = int(self.headers['content-length'])
                data_string = self.rfile.read(length)
                try:
                        result = data_string.decode('utf-8')
                        CommandExecutor.interpret(result)
                        #command_dict[result]()
                        print(result)
                except Exception as e:
                        print(e)
                        result = 'error'
                self.wfile.write(bytes(result, 'utf-8'))

         def do_GET(self):
                if self.path == '/':
                        self.send_response(301)
                        self.send_header('Location', '/index.html')
                        self.end_headers()
                elif self.path == '/index.html':
                        content = shared.index.encode('utf-8')
                        self.send_response(200)
                        self.send_header('content-type', 'text/html')
                        self.send_header('content-length', len(content))
                        self.end_headers()
                        self.wfile.write(content)
                elif self.path == '/stream.mjpg':
                        self.send_response(200)
                        self.send_header('Age', 0)
                        self.send_header('Cache-Control', 'no-cache, private')
                        self.send_header('Pragma', 'no-cache')
                        self.send_header('Content-Type', 'multipart/x-mixed-replace; boundary=FRAME')
                        self.end_headers()
                        try:
                                while True:
                                        with shared.output.condition:
                                                shared.output.condition.wait()
                                                frame = shared.output.frame
                                        self.wfile.write(b'--FRAME\r\n')
                                        self.send_header('Content-Type', 'image/jpeg')
                                        self.send_header('Content-Length', len(frame))
                                        self.end_headers()
                                        self.wfile.write(frame)
                                        self.wfile.write(b'\r\n')
                                        #print('a')
                        except Exception as e:
                                logging.warning(
                                        'Removed streaming client %s: %s',
                                        self.client_address, str(e))

                elif self.path == '/myo.js':
                        content = shared.myo.encode('utf-8')
                        self.send_response(200)
                        self.send_header('content-type', 'application/javascript')
                        self.send_header('content-length', len(content))
                        self.end_headers()
                        self.wfile.write(content)
                elif self.path == '/myscript.js':
                        content = shared.myscript.encode('utf-8')
                        self.send_response(200)
                        self.send_header('content-type', 'application/javascript')
                        self.send_header('content-length', len(content))
                        self.end_headers()
                        self.wfile.write(content)
                else:
                        self.send_error(404)
                        self.end_headers()

class StreamingServer(socketserver.ThreadingMixIn, server.HTTPServer):
        allow_reuse_address = True
        daemon_threads = True


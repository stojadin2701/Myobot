import io
import os
import logging
import socketserver
import time

import shared

from threading import Condition
from http import server
from string import Template

from command_executor import CommandExecutor

class StreamingOutput(object):
    def __init__(self):
        self.frame = None
        #self.frame_num = 0
        self.buffer = io.BytesIO()
        self.condition = Condition()

    def write(self, buf):
        if buf.startswith(b'\xff\xd8'):
            # New frame, copy the existing buffer's content and notify all
            # clients it's available
            #shared.camera.annotate_text = str(self.frame_num)
            #self.frame_num += 1
            self.buffer.truncate()
            with self.condition:
                self.frame = self.buffer.getvalue()
                self.condition.notify_all()
            self.buffer.seek(0)
        return self.buffer.write(buf)

class StreamingHandler(server.BaseHTTPRequestHandler):
    CONTENT_TYPES = {
        '.html': 'text/html',
        '.htm': 'text/html',
        '.js': 'application/javascript',
        '.css': 'text/css',
        '.txt': 'text/plain',
        '.text': 'text/plain',
        '.gif': 'image/gif',
        '.jpeg': 'image/jpeg',
        '.jpg': 'image/jpg',
        '.png': 'image/png'
    }

    def do_POST(self):
        length = int(self.headers['content-length'])
        data_string = self.rfile.read(length)
        try:
            print('received ajax request: '+ data_string.decode('utf-8'));
            result = shared.command_executor.interpret(data_string.decode('utf-8'))
            print(result)
        except Exception as e:
            print(e)
            result = 'error'
        if result is not None:
            self.wfile.write(result.encode('utf-8'))
            
    def do_GET(self):
        if self.path == '/':
            self.send_response(301)
            self.send_header('Location', '/index.html')
            self.end_headers()
        elif self.path == '/stream.mjpg':
            self.send_response(200)
            self.send_header('Age', 0)
            self.send_header('Cache-Control', 'no-cache, private')
            self.send_header('Pragma', 'no-cache')
            self.send_header('Content-Type', 'multipart/x-mixed-replace; boundary=FRAME')
            self.end_headers()
            try:
                frame_num = 0
                start = time.time()
                framerate = '...'
                while True:
                    with shared.output.condition:
                        shared.output.condition.wait()
                        frame = shared.output.frame
                    end = time.time()
                    shared.camera.annotate_text = '                                                                      fps: ' + str(framerate)
                    if end-start >= 1:
                        framerate = frame_num-1
                        start = time.time()
                        frame_num = 0                    
                    frame_num += 1
                    self.wfile.write(b'--FRAME\r\n')
                    self.send_header('Content-Type', 'image/jpeg')
                    self.send_header('Content-Length', len(frame))
                    self.end_headers()
                    self.wfile.write(frame)
                    self.wfile.write(b'\r\n')
            except Exception as e:
                logging.warning(
                    'Removed streaming client %s: %s',
                    self.client_address, str(e))
        elif os.path.exists('../Web'+self.path) and os.path.isfile('../Web'+self.path):
            if self.path == '/index.html':
                with io.open('../Web/index.html', 'r') as f:
                    content = f.read()
                Template(content).safe_substitute(dict(img_width=shared.config.get('web_params', 'img_width'), img_height=shared.config.get('web_params', 'img_height')))
                content = content.encode('utf-8')
                content_type = 'text/html'
            else:
                ext = os.path.splitext(self.path)[1]
                if ext in StreamingHandler.CONTENT_TYPES:
                    content_type = StreamingHandler.CONTENT_TYPES[ext]   
                else:
                    content_type = 'text/plain'

                with io.open('../Web'+self.path, 'rb') as f:
                    content = f.read()
                    
            self.send_response(200)
            self.send_header('content-type', content_type)
            self.send_header('content-length', len(content))
            self.end_headers()
            self.wfile.write(content)
        else:
            self.send_error(404)
            self.end_headers()

class StreamingServer(socketserver.ThreadingMixIn, server.HTTPServer):
    allow_reuse_address = True
    daemon_threads = True


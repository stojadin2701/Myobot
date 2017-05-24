import io
import picamera
import logging
import socketserver
from threading import Condition
from http import server


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
                        result = data_string.decode('utf-8') + ' :D'
                except:
                        result = 'error'
                self.wfile.write(bytes(result, 'UTF-8'))

         def do_GET(self):
                if self.path == '/':
                        self.send_response(301)
                        self.send_header('Location', '/index.html')
                        self.end_headers()
                elif self.path == '/index.html':
                        content = index.encode('utf-8')
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
                                        with output.condition:
                                                output.condition.wait()
                                                frame = output.frame
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

                elif self.path == '/myo.js':
                        content = myo.encode('utf-8')
                        self.send_response(200)
                        self.send_header('content-type', 'application/javascript')
                        self.send_header('content-length', len(content))
                        self.end_headers()
                        self.wfile.write(content)
                elif self.path == '/myscript.js':
                        content = myscript.encode('utf-8')
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

with picamera.PiCamera(resolution='1240x720', framerate=24) as camera:
        output = StreamingOutput()
        camera.start_recording(output, format='mjpeg')
        with io.open('index.html', 'r') as f:
                index = f.read()
        with io.open('myo.js', 'r') as f:
                myo = f.read()
        with io.open('myscript.js', 'r') as f:
                myscript = f.read()

        try:
                address = ('', 8080)
                server = StreamingServer(address, StreamingHandler)
                server.serve_forever()
        finally:
                camera.stop_recording()


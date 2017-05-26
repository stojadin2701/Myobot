import shared

class CommandExecutor(object):
    @staticmethod
    def interpret(command):
        if command == 'start_stream':
            shared.camera.start_recording(shared.output, format = 'mjpeg')
        elif command == 'stop_stream':
            shared.camera.stop_recording()

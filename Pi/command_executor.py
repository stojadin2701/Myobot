import shared

from motors import Motors

command_dict = {
        'forward': Motors.go_forward,
        'backward': Motors.go_backward,
        'left': Motors.turn_left,
        'right': Motors.turn_right,
        'stop': Motors.stop,
        'armband_disconnected': Motors.stop,
        'armband_unsynced': Motors.stop
    }

class CommandExecutor(object):    

    @staticmethod
    def interpret(command):
        if command in command_dict:
            command_dict[command]()
            result = command
        elif command == 'start_stream':
            shared.camera.start_recording(shared.output, format = 'mjpeg')
            result = command
        elif command == 'stop_stream':
            shared.camera.stop_recording()
            result = command
        elif command == 'distance_request':
            result = shared.receiver_thread.get_last_distance()
        else:
            result = command
        """
        elif command == 'stop_stream':
            shared.camera.stop_recording()
            result = None
        elif command == 'forward':
            result = 'going forward'
            Motors.go_forward()
        elif command == 'backward':
            result = 'going backward'
            Motors.go_backward()
        elif command == 'left':
            result = 'turning left'
            Motors.turn_left()
        elif command == 'right':
            result = 'turning right'
            Motors.turn_right()
        elif command == 'stop':
            result = 'stopping'
            Motors.stop()
        elif command == 'distance_request':
            result = shared.receiver_thread.get_last_distance()
        else:
            #Motors.stop()
            result = command
        """
        
        return result

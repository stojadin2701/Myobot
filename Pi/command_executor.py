import shared

from distance_sensor import DistanceSensor

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


class CommandExecutor(object):
    @staticmethod
    def interpret(command):
        if command == 'start_stream':
            shared.camera.start_recording(shared.output, format = 'mjpeg')
            result = None
        elif command == 'stop_stream':
            shared.camera.stop_recording()
            result = None
        elif command == 'fingers_spread':
            result = 'going forward'
        elif command == 'wave_in':
            result = 'turning left'
        elif command == 'wave_out':
            result = 'turning right'
        elif command == 'fist':
            result = 'going backward'
        elif command == 'double tap':
            result = 'options...'
        elif command == 'distance_request':
            result = shared.distance_thread.get_last_distance()
        else:
            result = command
        return result

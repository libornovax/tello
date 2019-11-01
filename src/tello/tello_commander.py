"""
Available Tello commands:

 * takeoff
 * land
 * emergency
 * up x
 * down x
 * left x
 * right x
 * forward x
 * back x
 * cw x
 * ccw x
 * flip x
 * go x y z speed
 * curve x1 y1 z1 x2 y2 z2 speed
 * rc a b c d

"""
import socket

from tello.utils import TELLO_IP, TELLO_COMMAND_PORT


class TelloCommander(object):

    def __init__(self):
        super(TelloCommander, self).__init__()

        self._socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._socket.connect((TELLO_IP, TELLO_COMMAND_PORT))
        # Send "command" to initialize the Tello SDK mode
        self.send("command")

    # ------------------------------------- PUBLIC INTERFACE ------------------------------------- #

    def send(self, command):
        self._socket.send(command.encode())

    def receive(self):
        result = self._socket.recv(1024)
        print(result.decode())

    # ------------------------------------ PRIVATE INTERFACE ------------------------------------- #

    def __del__(self):
        self._socket.close()

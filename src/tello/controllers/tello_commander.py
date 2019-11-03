import socket

from tello.utils import TELLO_IP, TELLO_COMMAND_PORT


class TelloCommander(object):
    """
    Object that provides easy interface for communication with the Tello drone, i.e. sending
    commands and receiving responses.
    """

    def __init__(self):
        super(TelloCommander, self).__init__()

        self._socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._socket.connect((TELLO_IP, TELLO_COMMAND_PORT))
        # Send "command" to initialize the Tello SDK mode
        self.send("command")

    # ------------------------------------- PUBLIC INTERFACE ------------------------------------- #

    def send(self, command):
        """
        Encodes and sends a command to the Tello drone.

        Args:
            command(str): String command (not encoded)
        """
        self._socket.send(command.encode())

    def receive(self):
        """
        Listens for a message from the Tello drone and returns once a message is obtained.

        Returns;
            :obj:`str` decoded message
        """
        result = self._socket.recv(1024)
        return result.decode()

    # ------------------------------------ PRIVATE INTERFACE ------------------------------------- #

    def __del__(self):
        self._socket.close()

import socket
import threading

from tello.synchronized_variable import SynchronizedVariable
from tello.utils import TELLO_IP, TELLO_COMMAND_PORT


class DataProvider(object):

    def __init__(self, port):
        super(DataProvider, self).__init__()
        # Internal data storage
        self._latest_data = SynchronizedVariable(None)
        self._latest_data_id = 0

        # Create and bind a socket to listen for all IPs on port 'port' (note: for some reason
        # binding directly the TELLO_IP does not work)
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._socket.bind(("", port))

        # Thread that is receiving messages via UDP and updates the value of the _latest_data
        self._thread = threading.Thread(target=self._thread_fn, daemon=True)

    # ------------------------------------- PUBLIC INTERFACE ------------------------------------- #

    def start(self):
        self._thread.start()
        # Send "command" to initialize the Tello SDK mode
        self._socket.sendto("command".encode(), (TELLO_IP, TELLO_COMMAND_PORT))

    def get_latest_data(self):
        data_dict = self._latest_data.value
        return (data_dict["id"], data_dict["data"]) if data_dict is not None else (None, None)

    # ------------------------------------ PRIVATE INTERFACE ------------------------------------- #

    def _thread_fn(self):
        raise NotImplementedError("Must be implemented by a child class!")

    def _set_latest_data(self, data):
        self._latest_data.value = self._create_new_data_dict(data)

    def _create_new_data_dict(self, data):
        self._latest_data_id += 1
        data_dict = {
            "id": self._latest_data_id,
            "data": data,
        }
        return data_dict

    def __del__(self):
        self._socket.close()

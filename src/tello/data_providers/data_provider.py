import socket
import threading

from tello.synchronized_variable import SynchronizedVariable
from tello.utils import TELLO_IP, TELLO_COMMAND_PORT


class DataProvider(object):
    """
    Base class for all data providers.

    Object that subscribes and creates a new thread to listen on the given port of the Tello drone.
    Internally stores and updates the latest data received from the drone.

    Args:
        port(int): Port of the Tello drone on which to listen
    """

    def __init__(self, port):
        super(DataProvider, self).__init__()
        # Internal data storage for latest data received by the receiver thread
        self._latest_data = SynchronizedVariable(None)
        # Counter for unique identifiers of the data
        self._latest_data_id = 0

        # Create and bind a socket to listen for all IPs on port `port` (note: for some reason
        # binding directly the TELLO_IP does not work)
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._socket.bind(("", port))

        # Thread that is receiving messages via UDP and updates the value of the `_latest_data`
        self._thread = threading.Thread(target=self._receiving_thread_fn, daemon=True)

    # ------------------------------------- PUBLIC INTERFACE ------------------------------------- #

    def start(self):
        """
        Start the receiving thread, which updates the latest received data.
        """
        self._thread.start()
        # Send "command" to initialize the Tello SDK mode
        self._socket.sendto("command".encode(), (TELLO_IP, TELLO_COMMAND_PORT))

    def get_latest_data(self):
        """
        Returns a unique id and the corresponding latest data stored in the provider.

        Returns:
            :obj:`int` unique id of the data (or None),
            :obj:`obj` latest data dependent on the implemented provider (or None)
        """
        data_dict = self._latest_data.value
        return (data_dict["id"], data_dict["data"]) if data_dict is not None else (None, None)

    # ----------------------------------- PROTECTED INTERFACE ------------------------------------ #

    def _receiving_thread_fn(self):
        """
        Function that runs on a separate thread and receives and updates the latest data.
        """
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

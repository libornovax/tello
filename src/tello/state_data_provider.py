from tello.data_provider import DataProvider
from tello.utils import TELLO_STATE_PORT


class StateDataProvider(DataProvider):

    def __init__(self):
        super(StateDataProvider, self).__init__(TELLO_STATE_PORT)

    def _thread_fn(self):
        while True:
            # Non-blocking receive because we want to update the latest data only if we get new data
            message, ip = self._socket.recvfrom(1024)
            self._set_latest_data(message.decode())

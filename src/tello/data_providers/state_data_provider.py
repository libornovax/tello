from tello.data_providers.data_provider import DataProvider
from tello.utils import TELLO_STATE_PORT


class StateDataProvider(DataProvider):

    def __init__(self):
        super(StateDataProvider, self).__init__(TELLO_STATE_PORT)

    # ------------------------------------ PRIVATE INTERFACE ------------------------------------- #

    def _thread_fn(self):
        while True:
            # Blocking receive because we want to update the latest data only if we get new data
            encoded_message, ip = self._socket.recvfrom(1024)
            # There can be leftover responses from initialization
            if encoded_message == "ok".encode():
                continue

            state_dict = self._state_message_to_dict(encoded_message.decode())

            self._set_latest_data(state_dict)

    def _state_message_to_dict(self, message):
        """
        Convert the string state message into a dictionary with keys and values.

        This is how the string message may look like:

        .. code::

            "mid:64;x:0;y:0;z:0;mpry:0,0,0;pitch:0;roll:0;yaw:42;vgx:0;vgy:0;vgz:0;templ:91;
            temph:93;tof:10;h:0;bat:69;baro:294.40;time:115;agx:-10.00;agy:-5.00;agz:-1000.00;\r\n"

        """
        state_dict = {}

        for key_value_str in message.split(";"):
            pair_data = key_value_str.split(":")
            if len(pair_data) == 2:
                state_dict[pair_data[0]] = float(pair_data[1])

        return state_dict

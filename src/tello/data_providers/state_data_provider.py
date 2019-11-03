from tello.data_providers.data_provider import DataProvider
from tello.utils import TELLO_STATE_PORT


class StateDataProvider(DataProvider):
    """
    Provider of the latest Tello state data in the form of a dictionary.

    The output state dictionary is indexed by the Tello native state variable names. All values are
    converted to float numbers. Therefore the output dictionary looks something like this:

    .. code ::

        {
            "x": 0.0,
            "y": 90.0,
            "z": 20.0,
            "bat": 90.0,
            "baro": 252.0,
            ...
        }

    """

    def __init__(self):
        super(StateDataProvider, self).__init__(TELLO_STATE_PORT)

    # ----------------------------------- PROTECTED INTERFACE ------------------------------------ #

    def _thread_fn(self):
        """
        Read state messages from the Tello drone and update the latest data with the newest state
        information dictionary.
        """
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

        This is how the string message from the Tello drone may look like:

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

import numpy as np

from tello.lib.libh264decoder import H264Decoder
from tello.data_providers.data_provider import DataProvider
from tello.utils import TELLO_CAMERA_PORT, TELLO_IP, TELLO_COMMAND_PORT


class CameraDataProvider(DataProvider):
    """
    Provider of the latest RGB camera image from the Tello drone as :obj:`np.array` with shape
    (height x width x 3).

    .. note::

        Internally the camera provider works like this: It collects all messages (data) belonging to
        a single image frame. The data is encoded with H264 so an H264 decoder is used to decode the
        content of the collected data. Finally, the decoded data is converted into a numpy array.

    """

    def __init__(self):
        super(CameraDataProvider, self).__init__(TELLO_CAMERA_PORT)

        self.decoder = H264Decoder()

    # ------------------------------------- PUBLIC INTERFACE ------------------------------------- #

    def start(self):
        super(CameraDataProvider, self).start()
        # Trigger the streaming service of the drone
        self._socket.sendto("streamon".encode(), (TELLO_IP, TELLO_COMMAND_PORT))

    # ----------------------------------- PROTECTED INTERFACE ------------------------------------ #

    def _receiving_thread_fn(self):
        """
        Collect and decode camera images frames from the Tello drone and update the latest data with
        the newest camera image.
        """
        while True:
            encoded_frame_data = self._collect_frame_data()

            decoded_frames = self.decoder.decode(encoded_frame_data)

            if decoded_frames:
                # Unpack the latest frame from the output of the H264 decoder (there should be only
                # one, but it returns an array anyway)
                (decoded_frame, width, height, _) = decoded_frames[-1]
                rgb_image = self._decoded_frame_to_numpy(decoded_frame, width, height)

                self._set_latest_data(rgb_image)
            else:
                print("WARNING: No frames decoded!")

    def _collect_frame_data(self):
        """
        Keep receiving data from the bound socket until the end of one image frame. Then return it
        as one chunk of data for decoding.

        .. note::

            Go to https://github.com/dji-sdk/Tello-Python/blob/master/Tello_Video/tello.py for the
            original implementation.

        """
        frame_data = "".encode()  # Received data are binary strings

        while True:
            # Blocking receive because we want to update the latest data only if we get new data
            message, ip = self._socket.recvfrom(2048)
            # There can be leftover responses from initialization
            if message == "ok".encode():
                continue

            frame_data += message

            if len(message) != 1460:
                break

        return frame_data

    def _decoded_frame_to_numpy(self, decoded_frame, width, height):
        """
        Convert the decoded string into a (height x width x 3) RGB image.

        Args:
            decoded_frame(str): Decoded string from the H264 decoder
            width(int): Width of the image frame
            height(int): Height of the image frame

        Return:
            :obj:`np.array` RGB camera image (height x width x 3)
        """
        frame = np.fromstring(decoded_frame, dtype=np.ubyte, count=len(decoded_frame), sep="")
        rgb_image = frame.reshape((height, width, 3))
        return rgb_image

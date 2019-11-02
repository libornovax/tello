from pynput.keyboard import Listener

from tello.controllers.tello_commander import TelloCommander


COMMAND_TAKEOFF = "takeoff"
COMMAND_LAND = "land"
COMMAND_HOVER = "rc 0 0 0 0"
COMMAND_EMERGENCY = "emergency"

COMMAND_FLY_LEFT = "rc -60 0 0 0"
COMMAND_FLY_RIGHT = "rc 60 0 0 0"
COMMAND_FLY_FORWARD = "rc 0 60 0 0"
COMMAND_FLY_BACKWARD = "rc 0 -60 0 0"
COMMAND_FLY_UP = "rc 0 0 60 0"
COMMAND_FLY_DOWN = "rc 0 0 -60 0"
COMMAND_ROTATE_CLOCKWISE = "rc 0 0 0 100"
COMMAND_ROTATE_COUNTERCLOCKWISE = "rc 0 0 0 -100"


class KeyboardController(object):

    KEY_TO_COMMAND = {
        "left": COMMAND_FLY_LEFT,
        "right": COMMAND_FLY_RIGHT,
        "up": COMMAND_FLY_FORWARD,
        "down": COMMAND_FLY_BACKWARD,
        "w": COMMAND_FLY_UP,
        "a": COMMAND_ROTATE_COUNTERCLOCKWISE,
        "s": COMMAND_FLY_DOWN,
        "d": COMMAND_ROTATE_CLOCKWISE,
        "space": COMMAND_HOVER,
        "shift": COMMAND_TAKEOFF,
        "shift_l": COMMAND_TAKEOFF,
        "shift_r": COMMAND_LAND,
        "esc": COMMAND_EMERGENCY,
    }

    def __init__(self, tello_commander=None):
        super(KeyboardController, self).__init__()

        self._tello_commander = tello_commander if tello_commander is not None else TelloCommander()
        self._listener = Listener(on_press=self._on_press, on_release=self._on_release)

    # ------------------------------------- PUBLIC INTERFACE ------------------------------------- #

    def start(self):
        self._listener.start()

    def stop(self):
        self._listener.stop()

    def join(self):
        self._listener.join()

    # ------------------------------------ PRIVATE INTERFACE ------------------------------------- #

    def _on_press(self, key):
        try:
            self._tello_commander.send(self.KEY_TO_COMMAND[self._decode_key(key)])
        except KeyError:
            pass  # Handle keys that do not correspond to any commands

    def _on_release(self, key):
        # Command the drone to start hovering after an action key release.
        if self._decode_key(key) in ["left", "right", "up", "down", "w", "a", "s", "d"]:
            self._tello_commander.send(COMMAND_HOVER)

    def _decode_key(self, key):
        if hasattr(key, "char"):
            return str(key.char).lower()
        elif hasattr(key, "name"):
            return str(key.name).lower()

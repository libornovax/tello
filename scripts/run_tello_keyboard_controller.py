#!/usr/bin/env python
"""
Control Tello from Keyboard
===========================

This script allows you to control the Tello drone from your keyboard using the implementation of the
:obj:`KeyboardController` in this package.

"""

from tello.controllers import KeyboardController


def main():
    print("=" * 99)
    print("TELLO KEYBOARD CONTROLLER")
    print("=" * 99)

    keyboard_controller = KeyboardController()

    # Start the keyboard-listening thread. This will listen to key presses and send commands to the
    # Tello drone when action keys are pressed
    keyboard_controller.start()

    # Join the keyboard-listening thread in order to prevent the program from quitting
    keyboard_controller.join()


if __name__ == "__main__":
    main()

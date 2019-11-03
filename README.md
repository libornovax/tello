Tello Drone Python Tools
========================

This repository contains implementation of tools that provide convenient access to the Tello Drone
controls and data streams through the Tello SDK.

The implementations are based on or use:

 * https://github.com/dji-sdk/Tello-Python
 * https://github.com/DaWelter/h264decoder


Contents
--------

As a base of this repo I would consider a hopefully nice and clean implementation of:

 * `StateDataProvider` - provides access to the latest Tello state
 * `CameraDataProvider` - provides access to the latest decoded camera image from the drone
 * `KeyboardController` - class that allows you to control the Tello drone with the keyboard

You can find example usages in the `scripts` folder:

 * `run_tello_keyboard_controller.py` - sample usage of keyboard controller for Tello
 * `run_tello_data_providers.py` - sample usage of data providers (showing video and state)


Usage
-----

I recommend to pip install (as editable) the package into a virtual environment. In order to achieve
that you can do for example (after activating your virtual environment):
```
python setup.py develop
```
This will install the package `tello` into your virtual environment as an editable package and it
will also automatically install all Python dependencies. You should be almost ready to go.

There is however one extra pain that is needed to overcome in order to receive an decode the video
stream from the Tello Drone. That is, we need a H264 decoder. There is one included with this
repository in `thirdparty/h264decoder`, however you will most likely need to build it as it is a C++
library. Please open the [thirdparty/h264decoder/README.md](thirdparty/h264decoder/README.md) for
more information.


Philosophy
----------

The elements in this package were created in a way that they provide non-blocking access to the
states, commands, and controls of the Tello drone.

The idea was to allow the control loop frequency to be independent of the state and video refresh
frequencies, but still being able to access the latest data. On top of that, also to avoid problems
with buffering of the state messages in the UDP message queue, which could result in working with
outdated messages.

The current implementation allows us to do for example:
```
...

while True:
    camera_data_id, camera_data = camera_data_provider.get_latest_data()
    state_data_id, state_data = state_data_provider.get_latest_data()

    ...
```
Where the frequency of the `while` loop is independent of the frequency of the messages in the data
providers, but still allows us to tie our actions to only moments when new data is available.

Be sure to check out one of the demos!

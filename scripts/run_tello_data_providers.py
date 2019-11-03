#!/usr/bin/env python
"""
Display Tello State And Camera Image
====================================

This script allows you to show the state data and the camera image of the Tello drone using the
:obj:`StateDataProvider` and :obj:`CameraDataProvider`.

"""

import cv2

from tello.data_providers import StateDataProvider, CameraDataProvider


def main():
    print("=" * 99)
    print("TELLO DATA PROVIDERS")
    print("=" * 99)

    state_data_provider = StateDataProvider()
    camera_data_provider = CameraDataProvider()

    # Start the threads of the providers that will be receiving new messages from the Tello drone
    # and updating the latest state and image that were received
    state_data_provider.start()
    camera_data_provider.start()

    # We want to refresh our output with every new incoming camera image (refreshing it all the time
    # would not make sense as we would be printing and showing still the same data)
    latest_camera_data_id = None

    while True:
        camera_data_id, camera_data = camera_data_provider.get_latest_data()

        # Check if the data provider gave us different data than in the previous call
        if latest_camera_data_id != camera_data_id:
            print("CAMERA DATA ID: {}".format(camera_data_id))

            _, state_data = state_data_provider.get_latest_data()
            print(state_data)

            # Show the newest image using OpenCV
            cv2.imshow("Tello Camera Image", cv2.cvtColor(camera_data, cv2.COLOR_RGB2BGR))
            cv2.waitKey(1)

            # Don't forget to update the latest camera id - we don't want to render this image again
            latest_camera_data_id = camera_data_id


if __name__ == "__main__":
    main()

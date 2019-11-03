H264 Decoder Python Module
==========================

**NOTE**: The decoder is taken from https://github.com/DaWelter/h264decoder and changed to work
with **Python 3**:

 * In the decoder Python interface changed `PyString_AsString`, `PyString_FromStringAndSize`, and
   `PyString_Size` to `PyBytes_AsString`, `PyBytes_FromStringAndSize`, and `PyBytes_Size`
   respectively since the former is not supported in Python 3.
 * Changed input type of the `decode` method from `py::str` to `py::object` as sting handling is
   different in Python 3 and no longer accepts `bytes` input.
 * Moved source files to the `src` folder.
 * Migrated `CMakeLists.txt` to Python 3.7.


How To Build
------------

Building of the decoder is fairly easy once you have all the dependencies (those you have to install
yourselves). Once you have all the dependencies, you should be able to successfully do:
```
cd thirdparty/h264decoder/build
cmake ..
make
```

This will create a library file in the `build` folder (either `libh264decoder.so` or
`libh264decoder.dylib` depending on which platform you are).


How To Use with The `tello` Package
-----------------------------------

In the `tello` package, the `src/tello/lib/libh264decoder.so` symlink is pointed by default to the
built `thirdparty/h264decoder/build/libh264decoder.dylib` library file. Therefore:

 * If your build step created `libh264decoder.dylib`, you don't have to do anything. The symlink is
   still valid.
 * If your build step created `libh264decoder.so`, then you have to update the symlink to point to
   the newly created `libh264decoder.so` file.



README FROM THE ORIGINAL IMPLEMENTATION
=======================================

The aim of this project is to provide a simple decoder for video
captured by a Raspberry Pi camera. At the time of this writing I only
need H264 decoding, since a H264 stream is what the RPi software 
delivers. Furthermore flexibility to incorporate the decoder in larger
python programs in various ways is desirable.

The code might also serve as example for libav and boost python usage.


Files
-----
* `h264decoder.hpp`, `h264decoder.cpp` and `h264decoder_python.cpp` contain the module code.

* Other source files are tests and demos.


Requirements
------------
* cmake for building
* libav
* boost python


Todo
----

* Add a video clip for testing and remove hard coded file names in demos/tests.


License
-------
The code is published under the Mozilla Public License v. 2.0. 

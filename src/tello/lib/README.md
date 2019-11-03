H264 Decoder (lib)
==================

The `lib` folder contains only a **symlink** to the actual *.so or *.dylib file, which you can
obtain by building the h264decoder library in the `thirdparty` folder of this repository.

**NOTE:** The symlink must be called `libh264decoder.so` on all platforms! Even if you are on macOS!
Otherwise Python will fail to import the library.

For further information please refer to the README in the `thirdparty/h264decoder` folder of this
repository.

cmake_minimum_required(VERSION 2.8)
project(python_h264decoder)

set(Python_ADDITIONAL_VERSIONS 3.7)
find_package(PythonInterp 3.7 REQUIRED)
find_package(PythonLibs 3.7 REQUIRED )
find_package(Boost REQUIRED COMPONENTS "python")

include_directories(${PYTHON_INCLUDE_DIRS})
include_directories(${Boost_INCLUDE_DIRS})
link_directories(${Boost_LIBRARY_DIRS})

add_compile_options ("-std=c++11")

add_library(h264decoder SHARED src/h264decoder.cpp src/h264decoder_python.cpp)
target_link_libraries(h264decoder avcodec swscale avutil ${Boost_PYTHON_LIBRARY_RELEASE} ${PYTHON_LIBRARIES})

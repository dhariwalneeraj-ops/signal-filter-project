cmake_minimum_required(VERSION 3.16)

project(signal_filter_project
    VERSION 1.0.0
    DESCRIPTION "Moving-average FIR filter using a circular buffer"
    LANGUAGES CXX
)

add_executable(signal_filter
    src/main.cpp
    src/MovingAverageFilter.cpp
)

target_include_directories(signal_filter PRIVATE include)
target_compile_features(signal_filter PRIVATE cxx_std_17)

if(MSVC)
    target_compile_options(signal_filter PRIVATE /W4)
else()
    target_compile_options(signal_filter PRIVATE -Wall -Wextra -Wpedantic)
endif()

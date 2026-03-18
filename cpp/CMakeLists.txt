cmake_minimum_required(VERSION 3.10)

project(cofee_bot LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 11)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

add_executable(engine_controll
    src/engine_controll.cpp
    src/classes.h
)

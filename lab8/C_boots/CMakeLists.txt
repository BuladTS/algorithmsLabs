cmake_minimum_required(VERSION 3.21)
project(C_boost C)

set(CMAKE_C_STANDARD 99)

add_executable(C_boost main.c file_funcs.c file_funcs.h)
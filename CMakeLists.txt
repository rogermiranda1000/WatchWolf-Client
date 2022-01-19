cmake_minimum_required(VERSION 3.16)
project(tester)

set(CMAKE_CXX_STANDARD 11)
set(CMAKE_BUILD_TYPE DEBUG)

# Botcraft variables
set(BOTCRAFT_BUILD_EXAMPLES OFF CACHE BOOL "")

set(APP_ROOT_DIR ${CMAKE_CURRENT_SOURCE_DIR})
set(APP_ROOT_BOTCRAFT_DIR ${APP_ROOT_DIR}/deps/Botcraft)

add_subdirectory(${APP_ROOT_BOTCRAFT_DIR})

add_executable(tester main.cpp)

target_link_libraries(tester botcraft)
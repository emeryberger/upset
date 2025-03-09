cmake_minimum_required(VERSION 3.15)
project(upset LANGUAGES CXX)

#
# ─── OPTIONS ──────────────────────────────────────────────────────────
#

# Default to C++14 (adjust as desired)
set(CMAKE_CXX_STANDARD 14)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Generate position-independent code; required for shared libraries on many platforms
set(CMAKE_POSITION_INDEPENDENT_CODE ON)

#
# ─── INCLUDE DIRECTORIES ──────────────────────────────────────────────
#

include_directories(
  ${PROJECT_SOURCE_DIR}
  ${PROJECT_SOURCE_DIR}/include
)

include(FetchContent)
FetchContent_Declare(
  Heap-Layers
  GIT_REPOSITORY https://github.com/emeryberger/Heap-Layers.git
  GIT_TAG        master
)
FetchContent_MakeAvailable(Heap-Layers)
include_directories(${heap-layers_SOURCE_DIR})


include(FetchContent)
FetchContent_Declare(
  printf
  GIT_REPOSITORY https://github.com/emeryberger/printf.git
  GIT_TAG        master
)
FetchContent_MakeAvailable(printf)
include_directories(${printf_SOURCE_DIR})

set(UNIX_SOURCES
  ${heap-layers_SOURCE_DIR}/wrappers/gnuwrapper.cpp
  src/libupset.cpp
  ${printf_SOURCE_DIR}/printf.cpp
)

set(MACOS_SOURCES
  ${heap-layers_SOURCE_DIR}/wrappers/macwrapper.cpp
  src/libupset.cpp
  ${printf_SOURCE_DIR}/printf.cpp
)

if(APPLE)
  set(UPSET_SOURCES ${MACOS_SOURCES})
else()
  set(UPSET_SOURCES ${UNIX_SOURCES})
endif()

#
# ─── UPSET LIBRARY ────────────────────────────
#

add_library(upset SHARED ${UPSET_SOURCES})
# Link with pthread/dl on Unix-like systems; on Windows, CMake will adjust automatically
target_link_libraries(upset PRIVATE pthread dl)
# Output the final library name as libXXX.so/.dylib on most platforms
set_target_properties(upset PROPERTIES
  OUTPUT_NAME "upset"
)


#
# ─── USAGE ────────────────────────────────────────────────────────────
#
# Typical usage:
#   mkdir build && cd build
#   cmake -DCMAKE_BUILD_TYPE=Release ..
#   cmake --build .
#
# If you wish to enable replicated mode:
#   cmake -DBUILD_REPLICATED=ON ..
#
# You now have libdiehard, optionally libdieharder, and optionally
# libdieharder_r, as shared libraries.
#
# For Debug builds:
#   cmake -DCMAKE_BUILD_TYPE=Debug ..
#
# Adjust flags, definitions, or compiler features above as needed.
#
# ──────────────────────────────────────────────────────────────────────

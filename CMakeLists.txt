cmake_minimum_required(VERSION 3.15)
project(diehard LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 14)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_POSITION_INDEPENDENT_CODE ON)

#
# ─── FETCH DIEHARD ───────────────────────────────────────────────────────────────
#
include(FetchContent)

FetchContent_Declare(
  diehard
  GIT_REPOSITORY https://github.com/emeryberger/DieHard.git
  GIT_TAG        master
)
FetchContent_MakeAvailable(diehard)

#
# ─── ADD DIEHARD (BUILD IT FROM ITS "src" FOLDER) ───────────────────────────────
#
# DieHard’s CMakeLists.txt resides in the "src" directory.
#
add_subdirectory(${diehard_SOURCE_DIR}/src ${CMAKE_CURRENT_BINARY_DIR}/diehard-build)

#
# Rename the resulting DieHard library to "libdiehard" for consistency,
# and ensure it’s built as a normal dynamic library (SHARED).
# (If the DieHard CMakeLists defines a different target name, adjust accordingly.)
#
set_target_properties(diehard PROPERTIES
    PREFIX ""                 # Remove the default "lib" prefix on Linux/macOS
    OUTPUT_NAME "libdiehard"  # => "libdiehard.so" or "libdiehard.dylib"
)

#
# ─── INSTALLATION ───────────────────────────────────────────────────────────────
#
# Install the dynamic library into a "diehard/" folder, so that scikit-build
# places it in site-packages/diehard/ after `pip install .`.
# Once installed, you can do (on macOS):
#   DYLD_INSERT_LIBRARIES=/path/to/libdiehard.dylib python script.py
# or on Linux:
#   LD_PRELOAD=/path/to/libdiehard.so python script.py
#
install(TARGETS diehard
    LIBRARY DESTINATION upset # diehard
    RUNTIME DESTINATION upset # diehard
)

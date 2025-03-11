cmake_minimum_required(VERSION 3.15)
project(upset LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 14)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_POSITION_INDEPENDENT_CODE ON)

#
# ─── FETCH DEPENDENCIES ──────────────────────────────────────────────────────────
#
include(FetchContent)

# Heap-Layers
FetchContent_Declare(
  Heap-Layers
  GIT_REPOSITORY https://github.com/emeryberger/Heap-Layers.git
  GIT_TAG        master
)
FetchContent_MakeAvailable(Heap-Layers)
include_directories(${heap-layers_SOURCE_DIR})

#
# ─── SOURCES ─────────────────────────────────────────────────────────────────────
#
set(UNIX_SOURCES
  ${heap-layers_SOURCE_DIR}/wrappers/gnuwrapper.cpp
  src/libupset.cpp
)

set(MACOS_SOURCES
  ${heap-layers_SOURCE_DIR}/wrappers/macwrapper.cpp
  src/libupset.cpp
)

if(APPLE)
  set(UPSET_SOURCES ${MACOS_SOURCES})
else()
  set(UPSET_SOURCES ${UNIX_SOURCES})
endif()

#
# ─── BUILD A SHARED LIBRARY (NOT MODULE) ──────────────────────────────────────
#
# `SHARED` => A real dynamic library on macOS (Mach-O dylib),
#   so it can be injected via DYLD_INSERT_LIBRARIES.
#
# `MODULE` => A "bundle" on macOS, which CANNOT be injected. Avoid that.
#
add_library(upset SHARED ${UPSET_SOURCES})
target_link_libraries(upset PUBLIC pthread dl)

# Make final name "libupset" (=> "libupset.dylib" on macOS, "libupset.so" on Linux).
set_target_properties(upset PROPERTIES
    PREFIX ""       # Remove the default "lib" prefix
    OUTPUT_NAME "libupset"
)

#
# ─── INSTALLATION ───────────────────────────────────────────────────────────────
#
# Installs the library into the "upset/" folder so that scikit-build can place
# "libupset.dylib" (or ".so") in site-packages/upset/ after `pip install .`.
#
install(TARGETS upset
    LIBRARY DESTINATION upset
    RUNTIME DESTINATION upset
)

#
# ─── NOTES ──────────────────────────────────────────────────────────────────────
#
# After this is built & installed (via pip/scikit-build), you can do:
#   DYLD_INSERT_LIBRARIES=/path/to/libupset.dylib python script.py
# on macOS. Or, for Linux:
#   LD_PRELOAD=/path/to/libupset.so python script.py
#
# The critical fix: "SHARED" instead of "MODULE" so macOS sees a true .dylib.
#
# ────────────────────────────────────────────────────────────────────────────────

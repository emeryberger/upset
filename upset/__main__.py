# upset/__main__.py

import os
import platform
import site
import sys
import sysconfig
import subprocess

def find_libupset_in_site_packages():
    """
    Scans known site-packages directories for:
       upset/libdiehard.so
    or
       upset/libdiehard.dylib
    Returns the first match found, or None if not found.
    """
    candidates = set()

    # 1) System site-packages
    if hasattr(site, "getsitepackages"):
        for p in site.getsitepackages():
            candidates.add(p)

    # 2) User site-packages
    if hasattr(site, "getusersitepackages"):
        candidates.add(site.getusersitepackages())

    # 3) sysconfig-based
    for key in ("platlib", "purelib"):
        sp = sysconfig.get_paths().get(key)
        if sp:
            candidates.add(sp)

    for sp in candidates:
        so_path = os.path.join(sp, "upset", "libdiehard.so")
        if os.path.isfile(so_path):
            return so_path

        dylib_path = os.path.join(sp, "upset", "libdiehard.dylib")
        if os.path.isfile(dylib_path):
            return dylib_path

    return None

def main():
    # If already injected, just continue (avoid infinite recursion).
    if os.environ.get("DYLD_INSERT_LIBRARIES") or os.environ.get("LD_PRELOAD"):
        # This is the second pass. The library is already preloaded.
        # Just let the user's script or module run normally.
        return

    # If the user didn't provide any additional arguments,
    # we have nothing to run.
    if len(sys.argv) < 2:
        print("Usage: python -m upset [script_or_module] [args...]")
        sys.exit(1)

    # Figure out if user wants to run a module (-m X) or a script (X.py, etc.)
    args = sys.argv[1:]  # everything after '-m upset'

    # Construct the command line we want to relaunch with:
    # If the user gave '-m something', pass that along to python.
    # Otherwise, run 'python <script> <args>'.
    if args[0] == "-m":
        # e.g. python -m upset -m pytest --maxfail=1
        # becomes: python -m pytest --maxfail=1
        command = [sys.executable] + args
    else:
        # e.g. python -m upset setmeup.py
        # becomes: python setmeup.py
        command = [sys.executable] + args

    # Find the installed 'libupset' in site-packages.
    lib_path = find_libupset_in_site_packages()
    if not lib_path:
        print("ERROR: Could not find 'libdiehard.so' or '.dylib' in site-packages.\n"
              "       Did you run `pip install .` (or `pip install -e .`)?",
              file=sys.stderr)
        sys.exit(1)

    # Set the environment variable for injection.
    env = os.environ.copy()
    if platform.system() == "Darwin":
        env["DYLD_INSERT_LIBRARIES"] = lib_path
    elif platform.system() == "Linux":
        env["LD_PRELOAD"] = lib_path

    env["PYTHONMALLOC"] = "malloc"

    # Re-run the command with the new environment (library injected).
    # We do not come back here after this call - this is a second process run.
    # print(f"[INFO] Preloading library at: {lib_path}", file=sys.stderr)
    # print(f"[INFO] Re-launching command: {command}", file=sys.stderr)
    result = subprocess.run(command, env=env)
    sys.exit(result.returncode)

if __name__ == "__main__":
    main()

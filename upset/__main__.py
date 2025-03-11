import ctypes
import ctypes.util
import os
import platform
import sys
import subprocess

def preload_library_and_run(command):
    system = platform.system()
    
    if system == "Linux":
        env = os.environ.copy()
        env['LD_PRELOAD'] = 'libupset.so'
        return subprocess.run(command, env=env)
    
    elif system == "Darwin":  # macOS
        env = os.environ.copy()
        env['DYLD_INSERT_LIBRARIES'] = 'libupset.dylib'
        return subprocess.run(command, env=env)
    
    else:
        return subprocess.run(command)
    
def main():
    command = [sys.executable] + sys.argv
    if not os.environ.get('LD_PRELOAD') and not os.environ.get('DYLD_INSERT_LIBRARIES'):
        result = preload_library_and_run(command)
        sys.exit(result.returncode)

if __name__ == "__main__":
    main()
    
                

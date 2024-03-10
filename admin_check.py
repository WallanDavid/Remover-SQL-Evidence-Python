import ctypes
import os
import sys

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

if not is_admin():
    # Re-launching the script with admin privileges
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, os.path.abspath(__file__), None, 1)
else:
    # Calling the main script
    exec(open(os.path.join(os.path.dirname(__file__), "main.py")).read())

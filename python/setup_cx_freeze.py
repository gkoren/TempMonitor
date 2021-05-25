import sys
from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need fine tuning.
build_exe_options = {"packages": ["matplotlib"],
                     "excludes": ["tkinter","collections.abc"],
                     "includes": ["numpy","PyQt4.QtCore","PyQt4.QtGui","matplotlib","sip","sys"] }

# GUI applications require a different base on Windows (the default is for a
# console application).
base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(  name = "TempMonitor",
        version = "0.1",
        description = "Temperature monitoring GUI application",
        options = {"build_exe": build_exe_options},
        executables = [Executable("Temp_monitor.py", base=base)])

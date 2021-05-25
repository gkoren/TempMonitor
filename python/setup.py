#setup.pi
from distutils.core import setup
from glob import glob
import py2exe
import numpy,random,sys,Queue,csv,time,matplotlib
#sys.path.append("C:\\Program Files\\Microsoft Visual Studio 9.0\\VC\\redist\\x86\\Microsoft.VC90.CRT")

setup(windows=[{"script":"Temp_monitor.py"}],
    options = {
        "py2exe": {

            "dll_excludes": ["MSVCP90.dll","libgdk_pixbuf-2.0-0.dll",'libgdk-win32-2.0-0.dll','libgobject-2.0-0.dll'],
            #"dll_excludes": ["libgdk_pixbuf-2.0-0.dll",'libgdk-win32-2.0-0.dll','libgobject-2.0-0.dll'],
            "packages": ["matplotlib","numpy"],
            "includes": ["numpy","PyQt4.QtCore","PyQt4.QtGui","matplotlib","sip"]
        }
    },
    data_files=matplotlib.get_py2exe_datafiles()
)
#matplotlib.get_py2exe_datafiles())
#("Microsoft.VC90.CRT", glob(r'C:\Program Files\Microsoft Visual Studio 9.0\VC\redist\x86\Microsoft.VC90.CRT\*.*')

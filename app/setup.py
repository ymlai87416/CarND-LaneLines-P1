from cx_Freeze import setup, Executable
import os

os.environ['TCL_LIBRARY'] = r"C:\Users\ymlai\Anaconda3\tcl\tcl8.6"
os.environ['TK_LIBRARY'] = r"C:\Users\ymlai\Anaconda3\tcl\tk8.6"
# Dependencies are automatically detected, but it might need
# fine tuning.
buildOptions = dict(
    packages = [],
    excludes = ["matplotlib", "IPython", "matplotlib.backends.backend_qt5agg", "tcl", "tk", "sqlite3", "ipykernel", "jupyter_client", "jupyter_core", "pydoc_data", "tkinter", "ipython_genutils", "ipywidgets"],
    includes = ["atexit", 'numpy.core._methods', 'numpy.lib.format', "pygments.lexers.python", "pygments.formatters.html"],
    include_files = []
)

import sys
base = 'Win32GUI' if sys.platform=='win32' else None

executables = [
    Executable(r'C:\GitProjects\CarND-LaneLines-P1\app\testDualVideo\video.py', base=base, targetName = 'main.exe')
]

setup(name='self driving - detecting lanes',
      version = '1.0',
      description = 'elf driving - detecting lanes',
      options = dict(build_exe = buildOptions),
      executables = executables)

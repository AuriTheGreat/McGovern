import sys
from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need fine tuning.
build_exe_options = {"build_exe": "build/McGovern Windows", 
                     "include_files": ["resources", "scenario"],
                     "packages": ["scipy"],
                     #"excludes": ["tomli", "pluggy", "iniconfig", "exceptiongroup", "colorama", "attrs", "pytest"]
                     }

# base="Win32GUI" should be used only for Windows GUI app
base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(
    name="McGovern",
    version="0.1.2",
    author="AuriTheGreat",
    description="A political simulator game",
    options={"build_exe": build_exe_options},
    executables=[Executable("Main.py", base=base, target_name='McGovern.exe', icon="resources/gfx/icon.ico")],
)
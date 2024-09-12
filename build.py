# you can use this on windows if you don't have mingw make installed
import sys
import os

if len(sys.argv) > 1:
    if sys.argv[1] == "help":
        print("""Comands:
        help               -- show this and stop the program
        all                -- build all files
        <other>            -- change <other> to some thing like smrun to build only the smrun.py file""")
    elif sys.argv[1] == "all":
        os.system("pyinstaller --onefile smrun.py")
        os.system("pyinstaller --onefile ioasm.py")
        os.system("pyinstaller --onefile iolang.py")
    else:
        os.system(f"pyinstaller --onefile {sys.argv[1]}.py")
else:
    print(f"Usage: {sys.argv[0]} <command>")
    print("use 'help' to see all existing commands")
import sys
from os.path import dirname, abspath
from src.utils import set_path

# Get absolute path to resource, works for dev and for PyInstaller
set_path(getattr(sys, '_MEIPASS', dirname(abspath(__file__))))

from src.pong import Pong

if __name__ == '__main__':
    Pong().run()
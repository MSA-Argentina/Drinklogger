import pygtk
pygtk.require('2.0')
import os

from zaguan import Zaguan

def load_window():
    zaguan = Zaguan('http://127.0.0.1:5000/')
    zaguan.run()

if __name__ == "__main__":
    load_window()
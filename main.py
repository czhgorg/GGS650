import Tkinter
import turtle
import threading
import struct
from Windows import *

def main():

    #================Display polygons================
    #--------Set up a window--------
    win = Windows(702,500)
    #win.addLayer('data/USARivers', 'blue')
    #win.addLayer('data/SelectedUSARoads', 'red')
    #win.addLayer('riverRoads/river','blue')
    #win.addLayer('riverRoads/road','red')
    win.root.mainloop()

if __name__=='__main__':
    main()

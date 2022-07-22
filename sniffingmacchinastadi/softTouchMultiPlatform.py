import threading
import time
from readConfiguration import ConfigSectionMap
import queue
from kbhit import KBHit

RPi = True
DBG = False

import os

if os.name == 'nt':
    pass
else:
    os = 'LINUX'
    if RPi == True:
        import RPi.GPIO as GPIO

def printdbg(dbg):
    if DBG == True:
        print(dbg)


class ButtonThreadrPi(threading.Thread):
    def __init__(self, name, qs, fsm ):
        threading.Thread.__init__(self)

        self.kbd = KBHit()
        self.name = name
        self.btnconf= ConfigSectionMap("config.ini","buttonconsensus")
        
        self.pinButton = int(self.btnconf["gpio"])
        self.longPression = float(self.btnconf["long"])
        self.shortPression = float(self.btnconf["short"])

        self.elapsed = 0
        self.initial = 0 
        self.isPressedBtn = False
        self.trigger = 'None'

        self.qs = qs["toFSM"]
        self.fsm = fsm

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pinButton, GPIO.IN) 

    def run(self):
        print("Buongiorno")
        while True:
            if self.kbd.kbhit():
                c = self.kbd.getch()
                if c=='p':
                    self.trigger = 'RESET_BOARD'
                    printdbg(self.trigger)
                    if self.qs != None:
                        self.qs.put( self.trigger )
                elif c=='r':
                    self.trigger = 'TEMP_UP'
                    printdbg(self.trigger)
                    if self.qs != None:
                        self.qs.put( self.trigger )
                elif c=='f':
                    self.trigger = 'TEMP_DOWN'
                    printdbg(self.trigger)
                    if self.qs != None:
                        self.qs.put( self.trigger )
                elif c=='e':
                    self.trigger = 'PRG_BUTTON'
                    printdbg(self.trigger)
                    if self.qs != None:
                        self.qs.put( self.trigger )
                elif c=='d':
                    self.trigger = 'SEL_BUTTON'
                    printdbg(self.trigger)
                    if self.qs != None:
                        self.qs.put( self.trigger )
            time.sleep(0.5)
                    

class ButtonThreadPC(threading.Thread):
    def __init__(self, name, qs, fsm ):
        threading.Thread.__init__(self)
        from kbhit import KBHit
        self.kbd = KBHit()
        self.name = name

        self.btnconf= ConfigSectionMap("config.ini","buttonconsensus")
        
        self.longPression = float(self.btnconf["long"])
        self.shortPression = float(self.btnconf["short"])
        self.elapsed = 0
        self.initial = 0 
        self.isPressedBtn = False
        self.trigger = 'None'

        self.qs = qs
        self.fsm = fsm
    
    def run(self):
        while True:
            if self.kbd.kbhit():
                c = self.kbd.getch()
                if c=='p':
                    self.trigger = 'RESET_BOARD'
                    print(self.trigger)
                    if self.qs != None:
                        self.qs.put( self.trigger )
                elif c=='r':
                    self.trigger = 'TEMP_UP'
                    print(self.trigger)
                    if self.qs != None:
                        self.qs.put( self.trigger )
                elif c=='f':
                    self.trigger = 'TEMP_DOWN'
                    print(self.trigger)
                    if self.qs != None:
                        self.qs.put( self.trigger )
                elif c=='e':
                    self.trigger = 'PRG_BUTTON'
                    print(self.trigger)
                    if self.qs != None:
                        self.qs.put( self.trigger )
                elif c=='d':
                    self.trigger = 'SEL_BUTTON'
                    print(self.trigger)
                    if self.qs != None:
                        self.qs.put( self.trigger )
            time.sleep(0.5)
                    
if __name__ == '__main__':

    print("Soft Touch example")

    qs = {'toFSM'  : queue.Queue() }

    if RPi == True:
        thdButton = ButtonThreadrPi("Button1",qs,None)
    else:
        thdButton = ButtonThreadPC("Button1",qs,None)
    
    thdButton.start()

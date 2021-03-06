#! /usr/bin/env python
#  -*- coding: utf-8 -*-
#
# Support module generated by PAGE version 7.3
#  in conjunction with Tcl version 8.6
#    Jul 06, 2022 02:53:42 PM CEST  platform: Windows NT

import sys
import tkinter as tk
import tkinter.ttk as ttk
from tkinter.constants import *

import rpicommand
import serial

#SERNAME = "/dev/ttyAMA0"
SERNAME = "COM1"
ser = ""

# ser = serial.Serial(SERNAME)  
# ser.baudrate = 9600
# data = ser.read()
# ser.write(data)
# ser.close()


def main(*args):
    '''Main entry point for the application.'''
    global root
    root = tk.Tk()
    root.protocol( 'WM_DELETE_WINDOW' , root.destroy)
    # Creates a toplevel widget.
    global _top1, _w1
    _top1 = root
    _w1 = rpicommand.Toplevel1(_top1)
    root.mainloop()

def doOff(*args):
    print('rpicommand_support.doOff')
    for arg in args:
        print ('another arg:', arg)
    sys.stdout.flush()

def doOn(*args):
    print('rpicommand_support.doOn')
    for arg in args:
        print ('another arg:', arg)
    sys.stdout.flush()

def doProg(*args):
    print('rpicommand_support.doProg')
    for arg in args:
        print ('another arg:', arg)
    sys.stdout.flush()

def doSel(*args):
    print('rpicommand_support.doSel')
    for arg in args:
        print ('another arg:', arg)
    sys.stdout.flush()

def doTMinus(*args):
    print('rpicommand_support.doTMinus')
    for arg in args:
        print ('another arg:', arg)
    sys.stdout.flush()

def doTplus(*args):
    print('rpicommand_support.doTplus')
    for arg in args:
        print ('another arg:', arg)
    sys.stdout.flush()

def openSerial(*args):
    print('rpicommand_support.openSerial')
    for arg in args:
        print ('another arg:', arg)

    try :
        global ser
        ser = serial.Serial(SERNAME)  
        ser.baudrate = 9600

        _w1.display.configure(text='''Opened Serial''')

    except:
        _w1.display.configure(text='''Error Opening Serial''')


    sys.stdout.flush()

def closeSerial(*args):
    print('rpicommand_support.closeSerial')
    for arg in args:
        print ('another arg:', arg)

    global ser
    try:
        ser.close()
        _w1.display.configure(text='''Closed Serial''')
    except:
        _w1.display.configure(text='''Error Closing Serial''')

    sys.stdout.flush()



def getSerial(*args):
    print('rpicommand_support.closeSerial')
    for arg in args:
        print ('another arg:', arg)

    global ser

    if (ser.in_waiting() > 0):
            data_str = ser.read(ser.in_waiting()).decode('ascii') 


    sys.stdout.flush()

if __name__ == '__main__':
    rpicommand.start_up()


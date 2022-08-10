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
import time

SERNAME = "/dev/ttyUSB0"
#SERNAME = "/dev/ttyAMA0"
#SERNAME = "COM1"
ser = ""

pathTemperature = "/home/pi/Desktop/RaspiFy/Enviroment/serviceAux.txt"

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

# def doOff(*args):
#     print('rpicommand_support.doOff')
#     for arg in args:
#         print ('another arg:', arg)
        
#     ser.write("e".encode())
    
#     sys.stdout.flush()

# def doOn(*args):
#     print('rpicommand_support.doOn')
#     for arg in args:
#         print ('another arg:', arg)
    
    
#     ser.write("e".encode())
#     sys.stdout.flush()
    

def doProg(*args):
    print('rpicommand_support.doProg')
    for arg in args:
        print ('another arg:', arg)
        
    ser.write("e".encode())
    getSerial()
    sys.stdout.flush()

def doSel(*args):
    print('rpicommand_support.doSel')
    for arg in args:
        print ('another arg:', arg)
    
    ser.write("d".encode())
    getSerial()
    sys.stdout.flush()

def doTMinus(*args):
    print('rpicommand_support.doTMinus')
    for arg in args:
        print ('another arg:', arg)
    
    ser.write("f".encode())
    getSerial()
    sys.stdout.flush()

def doTplus(*args):
    print('rpicommand_support.doTplus')
    for arg in args:
        print ('another arg:', arg)
    
    ser.write("r".encode())
    getSerial()
    sys.stdout.flush()


def r1on(*args):
    print('rpicommand_support.doTplus')
    for arg in args:
        print ('another arg:', arg)
    
    ser.write("q".encode())
    
    sys.stdout.flush()


def r1off(*args):
    print('rpicommand_support.doTplus')
    for arg in args:
        print ('another arg:', arg)
    
    ser.write("w".encode())
    
    sys.stdout.flush()


def r2on(*args):
    print('rpicommand_support.doTplus')
    for arg in args:
        print ('another arg:', arg)
    
    ser.write("a".encode())
    
    sys.stdout.flush()


def r2off(*args):
    print('rpicommand_support.doTplus')
    for arg in args:
        print ('another arg:', arg)
    
    ser.write("s".encode())
    
    sys.stdout.flush()

def r3off(*args):
    print('rpicommand_support.doTplus')
    for arg in args:
        print ('another arg:', arg)
    
    ser.write("x".encode())
    
    sys.stdout.flush()

def r3on(*args):
    print('rpicommand_support.doTplus')
    for arg in args:
        print ('another arg:', arg)
    
    ser.write("z".encode())
    
    sys.stdout.flush()

def getTemp(*args):
    print('rpicommand_support.gettemp')
    for arg in args:
        print ('another arg:', arg)

    try:
        f = open(pathTemperature, "r")
        string = f.readline()
        #print(string)
        utime = int(string.split(";")[0])
        temperature  = float(string.split(";")[1])
        hum = float(string.split(";")[2])
        print(utime,temperature,hum)
        from datetime import datetime
        print(datetime.utcfromtimestamp(utime).strftime('%Y-%m-%d %H:%M:%S'))
        _w1.displaytime.configure(text=datetime.utcfromtimestamp(utime).strftime('%Y-%m-%d %H:%M:%S'))
        _w1.displayaux.configure(text=string)
    except:
        print("Error")
        _w1.displaytime.configure(text="Error")
        _w1.displayaux.configure(text="Error")

    sys.stdout.flush()

def openSerial(*args):
    print('rpicommand_support.openSerial')
    for arg in args:
        print ('another arg:', arg)

    try :
        global ser
        ser = serial.Serial(SERNAME)
        ser.baudrate = 115200

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

def reset(*args):
    print('rpicommand_support.closeSerial')
    for arg in args:
        print ('another arg:', arg)
    
    # import subprocess
    import time

    # bashCommand = "sudo uhubctl -a 3 -l 2"
    # process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
    # output, error = process.communicate()

    import os
    os.system('sudo uhubctl -a 2 -l 2')


    time.sleep(5)

    sys.stdout.flush()



def getSerial(*args):
    print('rpicommand_support.getSerial')
    for arg in args:
        print ('another arg:', arg)

    global ser
    now = 0
    try:
        start=time.time()
        start = now
        timeout = 100
        
        #ser.write("SchermoONON".encode())

        while now - start < timeout:
            if (ser.inWaiting() > 0):
                data_str = ser.read(ser.inWaiting()).decode()
                lines = data_str.splitlines()
                print(data_str)
                _w1.display.configure(text=lines[-1])
            now=time.time()
    except:
        _w1.display.configure(text='''Serial Error''')

    sys.stdout.flush()

if __name__ == '__main__':
    rpicommand.start_up()


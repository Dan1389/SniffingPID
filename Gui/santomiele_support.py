#! /usr/bin/env python
#  -*- coding: utf-8 -*-
#
# Support module generated by PAGE version 7.3
#  in conjunction with Tcl version 8.6
#    Aug 02, 2022 04:46:17 PM CEST  platform: Windows NT

import sys
import tkinter as tk
import tkinter.ttk as ttk
from tkinter.constants import *
import paramiko
from scp import SCPClient
from tkinter import messagebox

import santomiele

def createSSHClient(server, port, user, password):
    client = paramiko.SSHClient()
    client.load_system_host_keys()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(server, port, user, password)
    return client

def main(*args):
    '''Main entry point for the application.'''
    global root
    root = tk.Tk()
    root.protocol( 'WM_DELETE_WINDOW' , root.destroy)
    # Creates a toplevel widget.
    global _top1, _w1
    _top1 = root
    _w1 = santomiele.Toplevel1(_top1)
    root.mainloop()

def GetDatas(*args):
    print('santomiele_support.GetDatas')
    for arg in args:
        print ('another arg:', arg)
    sys.stdout.flush()
    
    ipgreen = _w1.Entry1.get()
    try:
        ssh = createSSHClient(ipgreen, 22, "raspberry", "raspberry")
        scp = SCPClient(ssh.get_transport())

        #scp.put('sampletxt1.txt', 'sampletxt2.txt')
        scp.get('/home/raspberry/Desktop/test.txt')

        scp.close()
        messagebox.showinfo(title="Info", message="Correctly sended")
    except Exception as e :
        print(e)
        messagebox.showinfo(title="Info", message="Timeout Error")


def SetTemp(*args):
    print('santomiele_support.SetTemp')
    for arg in args:
        print ('another arg:', arg)

    ipgreen = _w1.Entry1.get()
    try:
        ssh = createSSHClient(ipgreen, 22, "raspberry", "raspberry")
        scp = SCPClient(ssh.get_transport())

        #scp.put('sampletxt1.txt', 'sampletxt2.txt')
        #scp.get('sampletxt2.txt')

        f = open("control.ini", "w+")
        f.write("[Control]\ntemp=" + _w1.Entry2.get())
        f.close()

        scp.put('control.ini', recursive=True, remote_path='/home/raspberry/Desktop/control.ini')

        scp.close()
        messagebox.showinfo(title="Info", message="Correctly sended")
    except Exception as e :
        print(e)
        messagebox.showinfo(title="Info", message="Timeout Error")

    
    sys.stdout.flush()

if __name__ == '__main__':
    santomiele.start_up()





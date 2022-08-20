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
from tkinter import filedialog
import os
import shutil
import re

import santomiele

usrname = "pi"
pwd = "raspberry"
pathLog = "./logGh" 


def create_directory(namedir):
    try:
        shutil.rmtree(namedir)
    except Exception as e:
        print(e)
    try:
        os.mkdir(namedir)
    except OSError:
        print ("Creation of the directory %s failed" % namedir)
    else:
        print ("Successfully created the directory %s " % namedir)


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
    create_directory(pathLog)
    root.mainloop()

def GetDatas(*args):
    print('santomiele_support.GetDatas')
    for arg in args:
        print ('another arg:', arg)
    sys.stdout.flush()

    ipgreen = _w1.Entry1.get()
    try:
        ssh = createSSHClient(ipgreen, 22, usrname, pwd)
        scp = SCPClient(ssh.get_transport())
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(ipgreen, username=usrname, password=pwd)

        stdin, stdout, stderr = ssh.exec_command('python3 /home/'+ usrname + '/Desktop/excelino.py')
        
        for line in stdout:
            print(line.strip('\n'))

        #scp.put('sampletxt1.txt', 'sampletxt2.txt')
        ##aggiungere local path
        folder_local = filedialog.askdirectory()

        if folder_local == None:
            messagebox.showinfo(title="Info", message="Error in folder")
            return

        scp.get('/home/'+ usrname + '/Desktop/OutputExcel/cell1.csv',local_path=folder_local)
        scp.get('/home/'+ usrname + '/Desktop/OutputExcel/cell2.csv',local_path=folder_local)
        scp.get('/home/'+ usrname + '/Desktop/OutputExcel/cell3.csv',local_path=folder_local)
        scp.get('/home/'+ usrname + '/Desktop/OutputExcel/cell4.csv',local_path=folder_local)
        scp.get('/home/'+ usrname + '/Desktop/OutputExcel/envi.csv',local_path=folder_local)
        try:
            scp.get('/home/'+ usrname + '/Desktop/OutputExcel/senseext.csv',local_path=folder_local)
        except:
            pass
        scp.close()
        ssh.close()
        messagebox.showinfo(title="Info", message="Correctly sent")
    except Exception as e :
        print(e)
        messagebox.showinfo(title="Info", message="Timeout Error")


def SetTemp(*args):
    print('santomiele_support.SetTemp')
    for arg in args:
        print ('another arg:', arg)

    ipgreen = _w1.Entry1.get()
    try:
        ssh = createSSHClient(ipgreen, 22, usrname , pwd)
        scp = SCPClient(ssh.get_transport())

        #scp.put('sampletxt1.txt', 'sampletxt2.txt')
        #scp.get('sampletxt2.txt')

        f = open("control.ini", "w+")
        try:
            tgui = float(_w1.Entry2.get())
            if tgui < 31 or tgui > 60:
                messagebox.showinfo(title="Info", message="Exceed limits")
                return
        except:
            messagebox.showinfo(title="Info", message="Wrong param")
            return
        f.write("[Control]\ntemp=" + _w1.Entry2.get())
        f.close()

        scp.put('control.ini', recursive=True, remote_path='/home/'+ usrname + '/Desktop/PythonScriptver2/sniffingmacchinastadi/control.ini')

        scp.close()
        messagebox.showinfo(title="Info", message="Correctly sent")
    except Exception as e :
        print(e)
        messagebox.showinfo(title="Info", message="Timeout Error")


    sys.stdout.flush()


def ReadLog(*args):
    print('santomiele_support.ReadLog')
    for arg in args:
        print ('another arg:', arg)

    ipgreen = _w1.Entry1.get()
    try:
        ssh = createSSHClient(ipgreen, 22, usrname , pwd)
        scp = SCPClient(ssh.get_transport())

        stdin, stdout, stderr = ssh.exec_command('python3 /home/'+ usrname + '/Desktop/ghlog.py')
        stdoutStr=stdout.readline()
        #print(stdoutStr,type(stdoutStr))
           
        result = re.search('Display aggiornato: (.*)', stdoutStr)
        #SENSORE INTERNO 2022-08-16 09:22:27   T:40.07 Hum:31.31 Fan:0   Display aggiornato: 25g      SENSORE ESTERNO 2022-08-16 09:22:27          T:30.5 Lux:16100.0 
        print(result)
        #disp = result.group(1)
        #print(result.group(1))
        
        try:
            disp = result.group(1)
            print(result.group(1))
            
            result = re.search('T:(.*) Hum:', stdoutStr)
            temp = result.group(1)
            print(result.group(1))

            if disp.find("g") > 0:
                state = "ON cooling"
            elif disp.find("r")>0:
                state = "ON heating"
            else:
                state ="OFF"
        except:
            
            state= "Error"

        _w1.Entry0.configure(state= "normal")
        _w1.Entry0.delete(0, 'end')
        #_w1.Entry0.insert(END,"T:" + str(temp) + " System:" + state )
        _w1.Entry0.insert(END," System:" + state )
        _w1.Entry0.configure(state= "disabled")

        scp.close()
        messagebox.showinfo(title="Info", message="Correctly sent")
    except Exception as e :
        print(e)
        messagebox.showinfo(title="Info", message="Timeout Error")


    sys.stdout.flush()

if __name__ == '__main__':
    santomiele.start_up()

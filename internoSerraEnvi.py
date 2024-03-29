import time 
import os
import serial
from datetime import datetime
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
RESET = 0
rst = True
GPIO.setup(RESET,GPIO.OUT)

#GPIO.output(RESET, rst)
#time.sleep(0.2)
GPIO.output(RESET, False)
time.sleep(0.2)
#GPIO.cleanup()


SERNAME = "/dev/ttyUSB0"
pathTemperature = "./greenhouse.txt"
pathFolder = "./logExt"
fileName = str(int(time.time())) + ".txt"
DELIMITER = ";"

def create_directory(namedir):
    try:
        os.mkdir(namedir)
    except OSError:
        print ("Creation of the directory %s failed" % namedir)
    else:
        print ("Successfully created the directory %s " % namedir)
        
def Rstboard(RESET,rst):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(RESET,GPIO.OUT)
        try:
            rst = not rst
            GPIO.output(RESET, rst)
            time.sleep(0.2)
            rst = not rst
            GPIO.output(RESET, rst)
            time.sleep(0.2)
            GPIO.cleanup()
            print("Inviato RST")
        except:
            print("Serial Error")
 

if __name__ == "__main__":
    
    try:
        #Rstboard(RESET,rst)
        #print("reset")
        create_directory(pathFolder)
        ser = serial.Serial(SERNAME)
        ser.baudrate = 9600

        print("serial opened")
        
        while True:

            f = open(pathTemperature, "w+")
            flog = open(pathFolder + "/" + fileName, "a+")
            
            timenow = int(time.time())
            s = ser.readline()
            s = s.strip()
            
            try:
                print (s.decode("utf-8"))
                finalstr = str(timenow) + DELIMITER + s.decode("utf-8")
                f.write(finalstr)
                flog.write(finalstr + "\n")
            except:
                f.write("Errore\n")
                print("Errore")
            f.close()
            flog.close()
            
            time.sleep(1)
    except Exception as e:
        print(e)

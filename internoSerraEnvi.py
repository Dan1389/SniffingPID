import time 
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
GPIO.cleanup()


SERNAME = "/dev/ttyUSB1"
pathTemperature = "./greenhouse.txt"
DELIMITER = ";"


if __name__ == "__main__":
    
    try:
        ser = serial.Serial(SERNAME)
        ser.baudrate = 9600

        print("serial opened")
        
        while True:

            f = open(pathTemperature, "w+")
            
            timenow = int(time.time())
            s = ser.readline()
            s = s.strip()
            
            try:
                print (s.decode("utf-8"))
                finalstr = str(timenow) + DELIMITER + s.decode("utf-8")
                f.write(finalstr)
            except:
                print("Errore")
            f.close()
            
            time.sleep(1)
    except Exception as e:
        print(e)

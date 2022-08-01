import time 
import serial
from datetime import datetime


SERNAME = "/dev/ttyUSB0"
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
            print (s.decode("utf-8"))
            
            
            finalstr = str(timenow) + DELIMITER + s.decode("utf-8")
            
            f.write(finalstr)
            f.close()
            
            time.sleep(1)
    except Exception as e:
        print(e)

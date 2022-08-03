import time 
import serial
from datetime import datetime
from kbhit import *

SERNAME = "/dev/ttyUSB0"
pathTemperature = "/home/raspberry/Desktop/RaspiFy/Enviroment/serviceAux.txt"

WAIT=1
WAIT_RESPONSE=1
        
def isnumber(x):
    if(x >= '0' and x <= '9'):
        return True
    else:
        return False
        
def commandos(cmd,ser):

    TX_ongoing=True
    disp=''
    try:
        ser.write(cmd.encode())
        print("sent "+cmd)
        time.sleep(WAIT_RESPONSE)
        while TX_ongoing:
            if (ser.inWaiting() > 0):
                data_str = ser.read(ser.inWaiting()).decode()
                lines = data_str.splitlines()

                for elm in lines:
                    print(elm)
                    if cmd == 'e':
                        if elm=="OFF":

                            disp=elm
                            TX_ongoing=False
                            break
                        if elm[3]=='g':

                            disp=elm
                            TX_ongoing=False
                            break 
                        if elm[3]=='r':

                            disp=elm
                            TX_ongoing=False
                            break                              
                    if cmd == 'd':
                        if elm[3]=='g':

                            disp=elm
                            TX_ongoing=False
                            break 
                        if elm[3]=='r':

                            disp=elm
                            TX_ongoing=False
                            break                        
                    if cmd == 'r':
                        if elm[0]=='G' and isnumber(elm[2]) and elm[3]=='g':
                            print("T+ cooling")
                            disp=elm
                            TX_ongoing=False
                            break 
                        if elm[0]=='d' and isnumber(elm[2]) and elm[3]=='r':
                            print("T+ heating")
                            disp=elm
                            TX_ongoing=False
                            break 
                    if cmd == 'f':
                        if elm[0]=='G' and isnumber(elm[2]) and elm[3]=='g':
                            print("T- cooling")
                            disp=elm
                            TX_ongoing=False
                            break
                        if elm[0]=='d' and isnumber(elm[2]) and elm[3]=='r':
                            print("T- heating")
                            disp=elm
                            TX_ongoing=False
                            break
                    if cmd=='m':
                        disp=elm
                        TX_ongoing=False
                        break
                    else:
                        TX_ongoing=False
                        break
                        
        return disp   
        
    except:
    
        print("ERRORE COMANDO")
        return False

if __name__ == "__main__":
    
    ser = serial.Serial(SERNAME)
    ser.baudrate = 115200

    print("serial opened")
    
    fan=0
    kb = KBHit()

    while True:

        if kb.kbhit():
            
            c = kb.getch()
            
            if c== 'e':
                print('pressed e')
                disp=commandos("e",ser)
                time.sleep(1)
                
            elif c== 'd':
                print('pressed d')
                disp=commandos("d",ser)
                time.sleep(1)
            
            elif c== 'r':
                print('pressed r')
                disp=commandos("r",ser)
                time.sleep(1)
                
            elif c== 'f':
                print('pressed f')
                disp=commandos("f",ser)
                time.sleep(1)
               
        else:    
            f = open(pathTemperature, "r")
            string = f.readline()

            utime = int(string.split(";")[0])
            temperature  = float(string.split(";")[1])
            hum = float(string.split(";")[2])
            date=datetime.utcfromtimestamp(utime).strftime('%Y-%m-%d %H:%M:%S')
            hours=date.split(" ")[1]
            h=int(hours.split(":")[0])
            
            time.sleep(WAIT)
            disp=commandos("m",ser)
            print(date,temperature,hum,disp,fan)
            
            if disp==False:
            
                print("ERRORE LETTURA SERIALE")
                
                while disp==False:
                    disp=commandos("m",ser)
                    time.sleep(WAIT)
                
            elif disp==" E3":
            
                print("ERRORE, accendi pompe e fan")
                
                ser.write("q".encode())
                fan=1
                time.sleep(WAIT)
                ser.write("a".encode())
                time.sleep(WAIT)
                ser.write("z".encode())
                time.sleep(WAIT)
            
            elif disp=="OFF":
            
                print("ACCENDI SISTEMA, accendi fan")
                
                try:
            
                    while disp=="OFF":
                        disp=commandos("e",ser)
                        time.sleep(WAIT)
                        
                    ser.write("q".encode())
                    fan=1
                    time.sleep(WAIT)
                
                except:
                    
                    print("ERRORE IN ACCENSIONE SISTEMA")
                    
            elif len(disp)>3: 
            
                if disp[3]=='g':
                
                    if (0<=h<7) or (h>17) :

                        print("metti in heat, accendi fan heat")
                        
                        try:
                        
                            while disp[3]=='g':
                                disp=commandos("d",ser)
                                time.sleep(WAIT)
                            
                            ser.write("q".encode())
                            time.sleep(WAIT)
                            fan=1
                            
                        except:

                            print("ERRORE IN SWITCH STATE HEAT")
                            
                    elif (7<=h<9) and  fan :
                    
                        print("spegni fan cold")
                        ser.write("w".encode())
                        fan=0
                        time.sleep(WAIT)

                    elif (9<=h<=17) and (not fan):

                        print("accendi fan cold")
                        ser.write("q".encode())
                        fan=1
                        time.sleep(WAIT)
                        
                elif disp[3]=='r':
                
                    if ((0<=h<7) or (h>17)) and (not fan) :

                        print("accendi fan heat")
                        ser.write("q".encode())
                        fan=1
                        time.sleep(WAIT)
                
                    elif (7<=h<9) :#and  fan :
                    
                        print("metti in cold, spegni fan cold ")
                        
                        try:
                    
                            while disp[3]=='r':
                                disp=commandos("d",ser)
                                time.sleep(WAIT)
                                   
                            ser.write("w".encode())
                            fan=0
                            time.sleep(WAIT)
                        
                        except:
                        
                            print("ERRORE IN SWITCH STATE COLD1")

                    elif (9<=h<=17) :#and (not fan):
                    
                        print("metti in cold, accendi fan cold")
                        
                        try:
                        
                            while disp[3]=='r':
                                disp=commandos("d",ser)
                                time.sleep(WAIT)

                            ser.write("q".encode())
                            fan=1
                            time.sleep(WAIT)
                        
                        except:
                            
                            print("ERRORE IN SWITCH STATE COLD2")
                                             
            else:
                
                print("SITUAZIONE NON CONTEMPLATA")

            
            time.sleep(5)
        



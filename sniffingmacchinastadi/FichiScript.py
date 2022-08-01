from transitions import Machine
from transitions import State 
import time
import threading
from controlc import install_handler
import serial
from datetime import datetime
WAIT_RESPONSE=1
WAIT_MANUAL = 1
WAIT = 1
DECISION_TRG = "DECISION_TIME"

HEAT_TIME_START= 17-1
HEAT_TIME_STOP=  8+1
COLDFAN_TIME_START= 10

def isnumber(x):
    if(x >= '0' and x <= '9'):
        return True
    else:
        return False

def commandos(cmd,ser,wait = WAIT_RESPONSE):

    TX_ongoing=True
    disp=''
    try:
        ser.write(cmd.encode())
        #print("sent "+cmd)
        time.sleep(wait)
        while TX_ongoing:
            if (ser.inWaiting() > 0):
                data_str = ser.read(ser.inWaiting()).decode()
                lines = data_str.splitlines()

                for elm in lines:
                    #print(elm)
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
        #print("ERRORE COMANDO")
        return False


class FichiMachine(Machine,threading.Thread):
    def __init__(self, qs , path , pathenv , serial, mode = ""):
        threading.Thread.__init__(self)
        self.qs = qs
        self.terminate = 0
        self.pathname = path
        self.pathnameenv = pathenv
        self.sername = serial
        self.ser = ""
        self.RSTCMD = "k"
        self.TUPCMD = "r"
        self.TDOCMD = "f"
        self.SELCMD = "d"
        self.PRGCMD = "e"
        self.FAN_ON ='q'
        self.FAN_OFF ='w'
        self.PUMP_ON ='a'
        self.PUMP_OFF ='s'
        self.PUMP2_ON ='z'
        self.PUMP2_OFF ='x'
        self.termoconv = 0
        self.pompa1 = 0
        self.pompa2 = 0
        self.display = ""
        #SENSORE AMBIENTE INTERNO
        self.utime = 0
        self.temperature = 0
        self.hum = 0
        self.hour = 0 
        #SENSORE AMBIENTE ESTERNO
        self.utimeenv = 0
        self.temperatureenv = 0
        self.lux = 0
        
        self.mode = mode
        
        while self.mode != 'a' and self.mode != 'm': 
            self.mode = input("--> inserisci modalita' [a/m]\n")
            print(self.mode)

        states=[
            State(name='Start'),
            State(name='Init',      on_enter=['Init'    ]),
            State(name='Idle',      on_enter=['Idle'    ]),
            State(name='PowerOn',   on_enter=['PowerOn' ]),
            State(name='Decision1',  on_enter=['Decision1']),
            State(name='Decision2',  on_enter=['Decision2']),
            State(name='Rstboard',  on_enter=['Rstboard']),
            State(name='Tupfun',    on_enter=['Tupfun'  ]),
            State(name='Tdownfun',  on_enter=['Tdownfun']),
            State(name='Prgfun',    on_enter=['Prgfun'  ]),
            State(name='Selfun',    on_enter=['Selfun'  ]),
            
            State(name='FanONfun',     on_enter=['FanONfun'  ]),
            State(name='FanOFFfun',    on_enter=['FanOFFfun'  ]),
            State(name='PumpONfun',    on_enter=['PumpONfun'  ]),
            State(name='PumpOFFfun',   on_enter=['PumpOFFfun'  ]),
            State(name='Pump2ONfun',   on_enter=['Pump2ONfun'  ]),
            State(name='Pump2OFFfun',  on_enter=['Pump2OFFfun'  ]),
            
            State(name='Error',     on_enter=['Error'   ]),
        ]

        transitions = [
            
            #Automatica
            # { 'trigger': 'LONG_SWITCH'  , 'source': 'Idle'        , 'dest': 'initWork'   }, 
            { 'trigger': 'START'        , 'source': 'Start'       , 'dest': 'Init'       }, 
            { 'trigger': 'DECISION_TIME', 'source': 'Idle'        , 'dest': 'Decision1'   }, 
            { 'trigger': 'DECISION_FUSION', 'source': 'Idle'        , 'dest': 'Decision2'   }, 
            { 'trigger': 'POWERON'      , 'source': 'Idle'        , 'dest': 'PowerOn'    }, 
            { 'trigger': 'READ_FILE'    , 'source': '*'           , 'dest': 'Idle'   },

            #Manuale
            { 'trigger': 'RESET_BOARD'  , 'source': '*'           , 'dest': 'Rstboard'   },
            { 'trigger': 'TEMP_UP'      , 'source': '*'           , 'dest': 'Tupfun'     },
            { 'trigger': 'TEMP_DOWN'    , 'source': '*'           , 'dest': 'Tdownfun'   },
            { 'trigger': 'PRG_BUTTON'   , 'source': '*'           , 'dest': 'Prgfun'     },
            { 'trigger': 'SEL_BUTTON'   , 'source': '*'           , 'dest': 'Selfun'     },
            { 'trigger': 'FAN_ON'       , 'source': '*'           , 'dest': 'FanONfun'     },
            { 'trigger': 'FAN_OFF'      , 'source': '*'           , 'dest': 'FanOFFfun'     },
            { 'trigger': 'PUMP_ON'      , 'source': '*'           , 'dest': 'PumpONfun'     },
            { 'trigger': 'PUMP_OFF'     , 'source': '*'           , 'dest': 'PumpOFFfun'     },
            { 'trigger': 'PUMP2_ON'     , 'source': '*'           , 'dest': 'Pump2ONfun'     },
            { 'trigger': 'PUMP2_OFF'    , 'source': '*'           , 'dest': 'Pump2OFFfun'     },
            { 'trigger': 'ERROR'        , 'source': '*'           , 'dest': 'Error' },
            
        ]

        Machine(self, states=states, transitions=transitions, ignore_invalid_triggers=True, initial='Start')

    def Idle(self) : 
        try:
            f = open(self.pathname , "r")
            string = f.readline()

            self.utime = int(string.split(";")[0])
            self.temperature  = float(string.split(";")[1])
            self.hum = float(string.split(";")[2])
            date=datetime.utcfromtimestamp(self.utime).strftime('%Y-%m-%d %H:%M:%S')
            hours=date.split(" ")[1]
            self.hour=int(hours.split(":")[0])+2
            f.close()
            print("SENSORE INTERNO")
            print("T,Hum,Display,Fan")
            print("----------------")
            print(date)
            print(self.temperature,self.hum,self.display,self.termoconv)
            print("----------------")
            if self.mode == 'a':
                self.display=commandos("m",self.ser)
                print("Display:",self.display)
        except:
            print("errore apertura file ambientale BME")

        try:
            f = open(self.pathnameenv , "r")
            string = f.readline()

            self.utimeenv = int(string.split(";")[0])
            self.temperatureenv  = float(string.split(";")[1])
            self.lux = float(string.split(";")[2])
            dateenv=datetime.utcfromtimestamp(self.utime).strftime('%Y-%m-%d %H:%M:%S')
            f.close()
            print("SENSORE ESTERNO")
            print("T,Lux")
            print("----------------")
            print(dateenv)
            print(self.temperatureenv,self.lux)
            print("----------------")
            
        except:
            print("errore apertura file ambientale LUX/T")

    ##############AUTOMATICO##################
       
    def Init(self) : 
        try:
            self.ser = serial.Serial(self.sername)
            self.ser.baudrate = 115200
            time.sleep(1)
            print("Serial opened")
            self.to_Idle()
        except:
            self.to_Error()
              
    def PowerOn(self) : 
        try:
            while self.display == "OFF":
                self.display = commandos("e",self.ser)
                time.sleep(WAIT)
                    
                ser.write("q".encode())
                self.termoconv=1
                time.sleep(WAIT)

        except:
            self.to_Error()
            print("Error")


    def Decision1(self) : 

        if self.display[3]=='g':
        
            if (0<=self.hour<HEAT_TIME_STOP) or (self.hour>HEAT_TIME_START) :

                print("metti in heat, accendi fan heat")
                try:
                
                    while self.display[3]=='g':
                        self.display=commandos("d",self.ser)
                        time.sleep(WAIT)
                    
                    self.ser.write("q".encode())
                    time.sleep(WAIT)
                    self.termoconv=1
                    
                except:
                    print("ERRORE IN SWITCH STATE HEAT")
                    self.to_Error()
                    
            elif (HEAT_TIME_STOP<=self.hour<COLDFAN_TIME_START) and self.termoconv :
            
                print("spegni fan cold")
                self.ser.write("w".encode())
                self.termoconv=0
                time.sleep(WAIT)

            elif (COLDFAN_TIME_START<=self.hour<=HEAT_TIME_START) and (not self.termoconv):

                print("accendi fan cold")
                self.ser.write("q".encode())
                self.termoconv=1
                time.sleep(WAIT)
                
        elif self.display[3]=='r':
        
            if ((0<=self.hour<HEAT_TIME_STOP) or (self.hour>HEAT_TIME_START)) and (not self.termoconv) :

                print("accendi fan heat")
                self.ser.write("q".encode())
                self.termoconv=1
                time.sleep(WAIT)
        
            elif (HEAT_TIME_STOP<=self.hour<COLDFAN_TIME_START) :#and  fan :
                print("metti in cold, spegni fan cold ")
                try:
                    while self.display[3]=='r':
                        self.display=commandos("d",self.ser)
                        time.sleep(WAIT)
                            
                    self.ser.write("w".encode())
                    self.termoconv=0
                    time.sleep(WAIT)
                
                except:
                    print("ERRORE IN SWITCH STATE COLD1")
                    self.to_Error()

            elif (COLDFAN_TIME_START<=self.hour<=HEAT_TIME_START) :#and (not fan):
                print("metti in cold, accendi fan cold")
                try:
                    while self.display[3]=='r':
                        self.display=commandos("d",self.ser)
                        time.sleep(WAIT)

                    self.ser.write("q".encode())
                    self.termoconv=1
                    time.sleep(WAIT)
                
                except:                    
                    print("ERRORE IN SWITCH STATE COLD2")
                    self.to_Error()

    def Decision2(self) : 
            pass

    ############MANUALE###########################
    def Rstboard(self) : 
        try:
            #self.ser.write(self.RSTCMD.encode())
#             self.display = commandos(self.RSTCMD,self.ser,WAIT_MANUAL)
#             print(self.display)
            print("Inviato RST")
        except:
            print("Serial Error")
       
    def Tupfun(self) : 
        try:
            #self.ser.write(self.TUPCMD.encode())
            self.display = commandos(self.TUPCMD,self.ser,WAIT_MANUAL)
            print(self.display)
            print("Inviato TUP")
        except:
            print("Serial Error")
       
    def Tdownfun(self) : 
        try:
            #self.ser.write(self.TDOCMD.encode())
            self.display = commandos(self.TDOCMD,self.ser,WAIT_MANUAL)
            print(self.display)
            print("Inviato TDOWN")
        except:
            print("Serial Error")
       
    def Prgfun(self) : 
        try:
            #self.ser.write(self.PRGCMD.encode())
            self.display = commandos(self.PRGCMD,self.ser,WAIT_MANUAL)
            print(self.display)
            print("Inviato ON/OFF")
        except:
            print("Serial Error")
              
    def Selfun(self) : 
        try:
            #self.ser.write(self.SELCMD.encode())
            self.display = commandos(self.SELCMD,self.ser,WAIT_MANUAL)
            print(self.display)
            print("Inviato SEL")
        except:
            print("Serial Error")
            
    def FanONfun(self) : 
        try:
            #self.ser.write(self.SELCMD.encode())
            self.ser.write("q".encode())
            time.sleep(WAIT)
            print(self.display)
            print("Inviato FUN ON")
        except:
            print("Serial Error")
            
    def FanOFFfun(self) : 
        try:
            #self.ser.write(self.SELCMD.encode())
            self.ser.write("w".encode())
            time.sleep(WAIT)
            print(self.display)
            print("Inviato FUN OFF")
        except:
            print("Serial Error")
    def PumpONfun(self) : 
        try:
            #self.ser.write(self.SELCMD.encode())
            self.ser.write("a".encode())
            time.sleep(WAIT)
            print(self.display)
            print("Inviato PUMP ON")
        except:
            print("Serial Error")
    def PumpOFFfun(self) : 
        try:
            #self.ser.write(self.SELCMD.encode())
            self.ser.write("s".encode())
            time.sleep(WAIT)
            print(self.display)
            print("Inviato PUMP OFF")
        except:
            print("Serial Error")
    def Pump2ONfun(self) : 
        try:
            #self.ser.write(self.SELCMD.encode())
            self.ser.write("z".encode())
            time.sleep(WAIT)
            print(self.display)
            print("Inviato PUMP2 ON")
        except:
            print("Serial Error")
    def Pump2OFFfun(self) : 
        try:
            #self.ser.write(self.SELCMD.encode())
            self.ser.write("x".encode())
            time.sleep(WAIT)
            print(self.display)
            print("Inviato PUMP2 OFF")
        except:
            print("Serial Error")  

    #####ERRORE#####
    def Error(self) : 
        try:
            self.ser.write("q".encode())
            time.sleep(WAIT)
            self.ser.write("a".encode())
            time.sleep(WAIT)
            self.ser.write("z".encode())
            time.sleep(WAIT)
            self.pompa1     = 1
            self.pompa2     = 1
            self.termoconv  = 1
            print("Errore Pompa di calore")
            self.to_Idle()
        except:
            print("Serial Error")
            print("Riavvio in: " + str(5))
            time.sleep(1)
            print("Riavvio in: " + str(4))
            time.sleep(1)
            print("Riavvio in: " + str(3))
            time.sleep(1)
            print("Riavvio in: " + str(2))
            time.sleep(1)
            print("Riavvio in: " + str(1))
            time.sleep(1)
            ## Riavvio
            self.to_Init()

    def run(self):

        self.trigger("START")

        while self.state != "Idle":
            pass

        while True:
            if self.mode == 'a':
                #DECISIONE STATO
                if self.display != False:
                    if self.display == " E3":
                        self.trigger("ERROR")
                    elif self.display == "OFF":
                        self.trigger("POWERON")
                    elif len(self.display)>3: 
                        self.trigger(DECISION_TRG)
                try:
                    item = self.qs["toFSM"].get(block=False)
                    self.trigger(item)  
                    self.qs["toFSM"].task_done()
                except:
                    print("coda vuota")
                time.sleep(4)
            else:
                try:
                    item = self.qs["toFSM"].get(block=False)
                    self.trigger(item)  
                    self.qs["toFSM"].task_done()
                except:
                    print("coda vuota")
        
            time.sleep(1)
            if self.state != "Error":
                self.trigger("READ_FILE")
                
if __name__ == '__main__':
    print("Florence And The finite state Machine")

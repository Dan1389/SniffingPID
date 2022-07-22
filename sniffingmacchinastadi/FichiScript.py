from transitions import Machine
from transitions import State 
import time
import threading
from controlc import install_handler
import serial
from datetime import datetime

WAIT_RESPONSE = 1
WAIT = 1
DECISION_TRG = "DECISION_TIME"

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
        #print("sent "+cmd)
        time.sleep(WAIT_RESPONSE)
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
    def __init__(self, qs , path, serial):
        threading.Thread.__init__(self)
        self.qs = qs
        self.terminate = 0
        self.pathname = path
        self.sername = serial
        self.ser = ""
        ####NON ME LI RICORDO###
        self.RSTCMD = ""
        self.TUPCMD = ""
        self.TDOCMD = ""
        self.SELCMD = ""
        self.PRGCMD = ""
        self.termoconv = 0
        self.pompa1 = 0
        self.pompa2 = 0
        self.display = ""
        self.utime = 0
        self.temperature = 0
        self.hum = 0
        self.hour = 0 
        
        self.mode = ""
        
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
            State(name='Error',     on_enter=['Error'   ]),
        ]

        transitions = [
        
            # { 'trigger': 'LONG_SWITCH'  , 'source': 'Idle'        , 'dest': 'initWork'   }, 
            { 'trigger': 'START'        , 'source': 'Start'       , 'dest': 'Init'       }, 
            { 'trigger': 'DECISION_TIME', 'source': 'Idle'        , 'dest': 'Decision1'   }, 
            { 'trigger': 'DECISION_FUSION', 'source': 'Idle'        , 'dest': 'Decision2'   }, 
            { 'trigger': 'POWERON'      , 'source': 'Idle'        , 'dest': 'PowerOn'    }, 
            { 'trigger': 'READ_FILE'    , 'source': '*'           , 'dest': 'Idle'   },

            { 'trigger': 'RESET_BOARD'  , 'source': '*'           , 'dest': 'Rstboard'   },
            { 'trigger': 'TEMP_UP'      , 'source': '*'           , 'dest': 'Tupfun'     },
            { 'trigger': 'TEMP_DOWN'    , 'source': '*'           , 'dest': 'Tdownfun'   },
            { 'trigger': 'PRG_BUTTON'   , 'source': '*'           , 'dest': 'Prgfun'     },
            { 'trigger': 'SEL_BUTTON'   , 'source': '*'           , 'dest': 'Selfun'     },
            
            { 'trigger': 'ERROR'        , 'source': '*'           , 'dest': 'Error' },
            
        ]

        Machine(self, states=states, transitions=transitions, ignore_invalid_triggers=True, initial='Start')

    def Idle(self) : 

        f = open(self.pathname , "r")
        string = f.readline()

        self.utime = int(string.split(";")[0])
        self.temperature  = float(string.split(";")[1])
        self.hum = float(string.split(";")[2])
        date=datetime.utcfromtimestamp(self.utime).strftime('%Y-%m-%d %H:%M:%S')
        hours=date.split(" ")[1]
        self.hour=int(hours.split(":")[0])
        f.close()
        print(date)
        print(self.temperature,self.hum,self.display,self.termoconv)
        
        if self.mode == 'a':
            self.display=commandos("m",self.ser)
            print(self.display)
    

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
        
            if (0<=self.hour<7) or (self.hour>17) :

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
                    
            elif (7<=self.hour<9) and self.termoconv :
            
                print("spegni fan cold")
                self.ser.write("w".encode())
                self.termoconv=0
                time.sleep(WAIT)

            elif (9<=self.hour<=17) and (not self.termoconv):

                print("accendi fan cold")
                self.ser.write("q".encode())
                self.termoconv=1
                time.sleep(WAIT)
                
        elif self.display[3]=='r':
        
            if ((0<=self.hour<7) or (self.hour>17)) and (not self.termoconv) :

                print("accendi fan heat")
                self.ser.write("q".encode())
                self.termoconv=1
                time.sleep(WAIT)
        
            elif (7<=self.hour<9) :#and  fan :
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

            elif (9<=self.hour<=17) :#and (not fan):
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
            self.ser.write(self.RSTCMD.encode())
            print("Inviato")
        except:
            print("Serial Error")
       
    def Tupfun(self) : 
        try:
            self.ser.write(self.TUPCMD.encode())
            print("Inviato")
        except:
            print("Serial Error")
       
    def Tdownfun(self) : 
        try:
            self.ser.write(self.TDOCMD.encode())
            print("Inviato")
        except:
            print("Serial Error")
       
    def Prgfun(self) : 
        try:
            self.ser.write(self.PRGCMD.encode())
            print("Inviato")
        except:
            print("Serial Error")
              
    def Selfun(self) : 
        try:
            self.ser.write(self.SELCMD.encode())
            print("Inviato")
        except:
            print("Serial Error")

    #####ERRORE#####
    def Error(self) : 
        try:
            ser.write("q".encode())
            time.sleep(WAIT)
            ser.write("a".encode())
            time.sleep(WAIT)
            ser.write("z".encode())
            time.sleep(WAIT)
            self.pompa1     = 1
            self.pompa2     = 1
            self.termoconv  = 1
            print("Errore Pompa di calore")
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
            else:
                item = self.qs["toFSM"].get()
                self.trigger(item)  
                self.qs["toFSM"].task_done()
        
            time.sleep(5)
            if self.state != "Error":
                self.trigger("READ_FILE")
                
if __name__ == '__main__':
    print("Florence And The finite state Machine")

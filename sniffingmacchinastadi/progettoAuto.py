from FichiScript import FichiMachine
from softTouchMultiPlatform import ButtonThreadrPi
import queue
from controlc import install_handler
from readConfiguration import ConfigSectionMap  

SERNAME = "/dev/ttyUSB0"
pathTemperature = "/home/pi/Desktop/RaspiFy/Enviroment/serviceAux.txt"
pathEnviro = "/home/pi/Desktop/PythonScriptver2/greenhouse.txt"

if __name__ == '__main__':
    
      print("Fichi Script Hello!")
      print("""----> Help: digita un comando per mettersi in modalità manuale, automatica altrimenti. <----\n 
            \t\t| p: RESET Pompa di calore \t|
            \t\t| r: T + \t\t\t|
            \t\t| e: T - \t\t\t|
            \t\t| f: On/Off \t\t\t|
            \t\t| q: Fan On \t\t\t|
            \t\t| a: Pompa 1 On \t\t\t|
            \t\t| z: Pompa 2 On \t\t\t|
            \t\t| w: Fan Off \t\t\t|
            \t\t| s: Pompa1 Off \t\t\t|
            \t\t| x: Pompa2 Off \t\t\t|
            \t\t| d: Caldo/Freddo \t\t|""")

      install_handler()

      qs = {'toFSM'  : queue.Queue() }

      workMachine = FichiMachine( qs,pathTemperature, pathEnviro ,SERNAME , mode = "a")
      thdButton = ButtonThreadrPi("Button", qs, workMachine)
      thdButton.start() 

      workMachine.start()
      print(workMachine.state)

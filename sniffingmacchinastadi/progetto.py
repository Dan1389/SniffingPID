from FichiScript import FichiMachine
from softTouchMultiPlatform import ButtonThreadrPi
import queue
from controlc import install_handler
from readConfiguration import ConfigSectionMap  

SERNAME = "/dev/ttyUSB0"
pathTemperature = "/home/raspberry/Desktop/RaspiFy/Enviroment/serviceAux.txt"


if __name__ == '__main__':
    
      print("Fichi Script Hello!")
      print("""----> Help: digita un comando per mettersi in modalità manuale, automatica altrimenti. <----\n 
            \t\t| p: RESET Pompa di calore \t|
            \t\t| r: T + \t\t\t|
            \t\t| e: T - \t\t\t|
            \t\t| f: On/Off \t\t\t|
            \t\t| d: Caldo/Freddo \t\t|""")

      install_handler()

      qs = {'toFSM'  : queue.Queue() }

      workMachine = FichiMachine( qs,pathTemperature,SERNAME )
      thdButton = ButtonThreadrPi("Button", qs, workMachine)
      thdButton.start() 

      workMachine.start()
      print(workMachine.state)
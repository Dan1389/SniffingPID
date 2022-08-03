import glob
import os
import pandas as pd
import shutil

#FOLDER IN WITH OUT FILES
outFolder = "/home/pi/Desktop/OutputExcel"

#TO SEARCH
pathext = "/home/pi/Desktop/PythonScriptver2/logExt/*"
pathcell1 = "/home/pi/Desktop/RaspiFy/cell1/*"
pathcell2 = "/home/pi/Desktop/RaspiFy/cell2/*"
pathcell3 = "/home/pi/Desktop/RaspiFy/cell3/*"
pathcell4 = "/home/pi/Desktop/RaspiFy/cell4/*"
pathenvi = "/home/pi/Desktop/RaspiFy/Enviroment/*"


#FINAL NAMES
nameext = "/senseext.csv"
namec1 = "/cell1.csv"
namec2 = "/cell2.csv"
namec3 = "/cell3.csv"
namec4 = "/cell4.csv"
nameenv = "/envi.csv"

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


def createLastmodCSV(path, out):
    list_of_files = glob.glob(path) 
    latest_file = max(list_of_files, key=os.path.getmtime)
    print(latest_file)
    read_file = pd.read_csv(latest_file)
    read_file.to_csv (out, index=None)


if __name__ == "__main__":

    create_directory(outFolder)
    createLastmodCSV(pathext,outFolder + nameext)
    createLastmodCSV(pathcell1,outFolder + namec1)
    createLastmodCSV(pathcell2,outFolder + namec2)
    createLastmodCSV(pathcell3,outFolder + namec3)
    createLastmodCSV(pathcell4,outFolder + namec4)
    createLastmodCSV(pathenvi,outFolder + nameenv)

import glob
import os

usrname = "pi"

path = '/home/'+ usrname + '/Desktop/PythonScriptver2/sniffingmacchinastadi/LogGreenhouse/*'


list_of_files = glob.glob(path) 
latest_file = max(list_of_files, key=os.path.getmtime)

with open(latest_file, "r") as file:
    last_line = file.readlines()[-1]

print(last_line)
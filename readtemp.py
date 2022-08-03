import time 

pathTemperature = "/home/pi/Desktop/RaspiFy/Enviroment/serviceAux.txt"


if __name__ == "__main__":
    while True:
        try:
            f = open(pathTemperature, "r")
            string = f.readline()
            #print(string)
            utime = int(string.split(";")[0])
            temperature  = float(string.split(";")[1])
            hum = float(string.split(";")[2])
            print(utime,temperature,hum)
        except:
            print("Error")
        time.sleep(10)
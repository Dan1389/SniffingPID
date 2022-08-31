from bluetooth import *
import time
import threading
            
pathTemperature = "./dewpoint.txt"
pathFolder = "./logDew"
fileName = str(int(time.time())) + ".txt"


def create_directory(namedir):
    try:
        os.mkdir(namedir)
    except OSError:
        print ("Creation of the directory %s failed" % namedir)
    else:
        print ("Successfully created the directory %s " % namedir)

def input_and_send(sock):
    print("\nType something\n")
    while True:
        data = input()
        if len(data) == 0: break
        sock.send(data)
        sock.send("\n")
        time.sleep(1)
        
def rx_and_echo(sock,buf_size):
    #sock.send("\nsend anything\n")
    t = ""

    while True:
        t+= sock.recv(buf_size).decode("utf-8")
        if len(t) == 30:

            f = open(pathTemperature, "w+")
            flog = open(pathFolder + "/" + fileName, "a+")
                
            timenow = int(time.time())
                
            s = t.replace("\n",'')
                
            try:
                finalstr = str(timenow) + ";" + s
                print(finalstr)
                f.write(finalstr)
                flog.write(finalstr + "\n")
            except:
                f.write("Errore\n")
                print("Errore")
            
            f.close()
            flog.close()
            
            t = ""
            #sock.send(data)
        
        time.sleep(1)
   


if __name__ == "__main__":
    try:
        while True:
        
            create_directory(pathFolder)
                
            #MAC address of ESP32
            addr = "24:6F:28:97:43:12"
            #uuid = "94f39d29-7d6d-437d-973b-fba39e49d4ee"
            #service_matches = find_service( uuid = uuid, address = addr )
            service_matches = find_service( address = addr )

            buf_size = 1024;

            while len(service_matches) == 0:
                print("couldn't find the SampleServer service =(")
                time.sleep(10)
                service_matches = find_service( address = addr )

            for s in range(len(service_matches)):
                print("\nservice_matches: [" + str(s) + "]:")
                print(service_matches[s])
                
            first_match = service_matches[0]
            port = first_match["port"]
            name = first_match["name"]
            host = first_match["host"]
         


            port=1
            print("connecting to \"%s\" on %s, port %s" % (name, host, port))

            # Create the client socket
            sock=BluetoothSocket(RFCOMM)
            sock.connect((host, port))

            print("connected")
            
            t1 = threading.Thread(target=rx_and_echo, args=[sock,buf_size])
            t2 = threading.Thread(target=input_and_send,args=[sock])
            
            #input_and_send()
            try:
                t1.start()
                t2.start()
            except:
                sock.close()
                print("Timeout")
    except:
        sock.close()
        print("\n--- bye ---\n")

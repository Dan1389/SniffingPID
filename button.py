import RPi.GPIO as GPIO
import time


switch = 6

GPIO.setmode(GPIO.BCM)
GPIO.setup(switch, GPIO.OUT)

while True:
    
    prp=input("PREMI A PER RESETTARE ")
    if prp=='a':
        print("reset")
        GPIO.output(switch, GPIO.HIGH)
        time.sleep(2)
        GPIO.output(switch, GPIO.LOW)
    else:
        pass
        


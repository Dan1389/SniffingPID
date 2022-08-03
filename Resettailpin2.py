import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)
LED = 0
ledState = True
GPIO.setup(LED,GPIO.OUT)

ledState = not ledState
GPIO.output(LED, ledState)
time.sleep(0.2)
ledState = not ledState
GPIO.output(LED, ledState)
time.sleep(0.2)
GPIO.cleanup()

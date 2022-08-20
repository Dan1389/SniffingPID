import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)
LED = 0
ledState = False
GPIO.setup(LED,GPIO.OUT)

ledState = not ledState
GPIO.output(LED, ledState)
time.sleep(0.3)
ledState = not ledState
GPIO.output(LED, ledState)
time.sleep(0.3)
GPIO.cleanup()

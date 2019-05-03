import threading
import RPi.GPIO as GPIO
import time

servoPIN = 17

class Servo(threading.Thread):

    def thread_servo(self):
        print('Thread servo iniciada')

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(servoPIN, GPIO.OUT)

        p = GPIO.PWM(servoPIN, 50) # GPIO 17 for PWM with 50Hz
        p.start(12.5) # Initialization
        time.sleep(5)
        
        p.ChangeDutyCycle(7)
        time.sleep(2)

## NAO ESTA NO GITHUB

import threading
import RPi.GPIO as GPIO
import time
import globals

class Motor(threading.Thread):

    def __init__(self):
        GPIO.setmode(GPIO.BCM)        
        GPIO.setup(pin, GPIO.OUT)
        
        #Garante que inicia o sistema com o motor off
        GPIO.output(pin, GPIO.HIGH)

    def thread_motor(self):
        print('Thread motor iniciada')
        pin = 21
        
        while not globals.eventoPorcaoServida.is_set():
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(pin, GPIO.OUT)
            #Ativa o motor
            GPIO.output(pin, GPIO.LOW)
            time.sleep(0.75)
            #Desativa
            GPIO.output(pin, GPIO.HIGH)
            time.sleep(1)            

        #Desativa
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, GPIO.HIGH)




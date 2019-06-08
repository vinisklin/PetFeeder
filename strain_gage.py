import threading
import RPi.GPIO as GPIO
import time
import sys
import globals
from hx711 import HX711

pin1 = 5
pin2 = 6
hx = HX711(pin1, pin2)

class Strain_gage(threading.Thread):

    def thread_strain_gage(self):
        print('Thread strain gage iniciada')

        hx.set_offset(8241335.0)
        hx.set_scale(206.07129798903108)

        peso = 0

        with globals.mutexPorcao:
            pesoDaPorcao = globals.pesoPorcao

        while peso < pesoDaPorcao:
            peso = max(0, (hx.get_grams() - 135)) ##135 peso do pote
            print('O peso eh de: ', peso)
        
            with globals.mutexPorcao:
                globals.pesoAtual = peso

            hx.power_down()
            time.sleep(.001)
            hx.power_up()

            time.sleep(0.5)

        print('Porcao servida')
        GPIO.cleanup()

        #Envia sinal para parar o motor e ativar camera
        globals.eventoPorcaoServida.set()
        
        time.sleep(3)
        globals.pesoAtual = 0 
            

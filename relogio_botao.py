import threading
import time
import datetime
# import RPi.GPIO as GPIO
import globals

horaAlimentar = datetime.time(15, 33)
botaoPin = 10

class Relogio_botao(threading.Thread):

    def button_callback(self):
        globals.eventoAlimentar.set()

    def thread_relogio_botao(self):
        #Configura o GPIO da Raspberry Pi
        # GPIO.setwarnings(False)
        # GPIO.setmode(GPIO.BOARD)
        # GPIO.setup(botaoPin, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
        # GPIO.add_event_detect(botaoPin, GPIO.RISING,
        #                       callback = self.button_callback,
        #                       debounce = 1000)

        while True:
            horaAtual = datetime.datetime.now().time()
            print(horaAtual)

            #Verifica se esta na hora de alimentar
            if ((horaAlimentar.hour == horaAtual.hour) and \
            (horaAlimentar.minute == horaAtual.minute)):
                globals.eventoAlimentar.set()

            time.sleep(20) # 60. Esta 5 apenas p teste

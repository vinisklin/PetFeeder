import threading
import time
import datetime
# import RPi.GPIO as GPIO
import globals

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
            with globals.mutexHora:
                if ((globals.horaAlimentar.hour == horaAtual.hour) and \
                (globals.horaAlimentar.minute == horaAtual.minute)):
                    #Envia sinal para main ativar as outras threads
                    globals.eventoAlimentar.set()
                    print('Hora do rango')

            time.sleep(60) # 60. Esta 5 apenas p teste

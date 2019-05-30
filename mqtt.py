import threading
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
import datetime
import time
import globals

class Mqtt(threading.Thread):

    def on_connect(self, client, userdata, flags, rc):
        print("Conectado ao Broker. Resultado de conexao: " + str(rc))

        # faz subscribe para receber msgs
        client.subscribe("PetFeeder/hora")
        client.subscribe("PetFeeder/porcao")
        client.subscribe("PetFeeder/servir")

    def on_message(self, client, userdata, msg):

        #Recebeu msg para servir agora-------------------------------------
        if msg.topic == 'PetFeeder/servir':
            globals.eventoAlimentar.set()

        #Recebeu nova hora de servir---------------------------------------
        if msg.topic == 'PetFeeder/hora':
            #Converte a msg em hora  
            hora = 10 * int(str(msg.payload)[2]) + int(str(msg.payload)[3])
            minuto = 10 * int(str(msg.payload)[4]) + int(str(msg.payload)[5])

            #Salva a nova hora na memoria e atualiza a variavel
            file = open('/home/pi/Downloads/Imagens/horaServir.txt','w')
            with globals.mutexHora:
                file.write(str(hora)+'\n')
                file.write(str(minuto)+'\n')
                file.close()
                globals.horaAlimentar = datetime.time(hora, minuto)
                print("Nova hora de servir: " + str(globals.horaAlimentar))

        #Recebeu nova quantidade de racao----------------------------------
        if msg.topic == 'PetFeeder/porcao':
            #Converte a msg em porcao  
            novaPorcao = (100 * int(str(msg.payload)[2])) + \
                (10 * int(str(msg.payload)[3])) + \
                int(str(msg.payload)[4])

            #Salva a nova porcao na memoria e atualiza a variavel
            file = open('/home/pi/Downloads/Imagens/pesoPorcao.txt','w')
            with globals.mutexPorcao:
                file.write(str(novaPorcao))
                file.close()
                globals.pesoPorcao = novaPorcao
                print("Novo peso da porcao: " + str(globals.pesoPorcao))


    def thread_mqtt(self):
        # inicializa MQTT:
        client = mqtt.Client('RaspberryClient')
        client.on_connect = self.on_connect
        client.on_message = self.on_message

        client.connect("iot.eclipse.org", 1883, 60)

        print('Thread mqtt iniciada')

        client.loop_start()

        while True:
            if globals.eventoNotificarPoteVazio.is_set():
                print("Notificando para o usuario que o pote esta vazio")
                publish.single("PetFeeder/poteVazio", "1", hostname='iot.eclipse.org')
                globals.eventoNotificarPoteVazio.clear()

            while globals.eventoAlimentar.is_set():
                #Fica enviando o peso que está sendo servido para o app
                with globals.mutexPorcao:
                    publish.single("PetFeeder/peso", globals.pesoAtual, hostname='iot.eclipse.org')
##                    print('Publicou: ', globals.pesoAtual)
                time.sleep(0.5)
            time.sleep(2)
            


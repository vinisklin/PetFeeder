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
        client.subscribe("PetFeeder/racao")

    def on_message(self, client, userdata, msg):

        #Recebeu msg para servir agora
        if msg.payload == b'servirRacao':
            globals.eventoAlimentar.set()

        #Recebeu nova hora de servir (72 = H)
        if msg.payload[0] == 72:
            #Escreve a hora recebida (-48 eh pq o valor ta em ASCII)
            hora = (msg.payload[1] - 48) * 10 + (msg.payload[2] - 48)
            minuto = (msg.payload[3] - 48) * 10 + (msg.payload[4] - 48)
            
            file = open('/home/pi/Downloads/Imagens/memory.txt','w')
            with globals.mutexHora:
                file.write(str(hora)+'\n')
                file.write(str(minuto)+'\n')
                file.close()
                globals.horaAlimentar = datetime.time(hora, minuto)
                print("Nova hora de servir: " + str(globals.horaAlimentar))

        #Recebeu nova quantidade de racao


    def thread_mqtt(self):
        # inicializa MQTT:
        client = mqtt.Client('RaspberryClient')
        client.on_connect = self.on_connect
        client.on_message = self.on_message

        client.connect("iot.eclipse.org", 1883, 60)

        print('Thread mqtt iniciada')

        client.loop_start()

        while True:
            if globals.eventoEnviarImg.is_set():
                #Prepara e envia a imagem para o aplicativo
                print("Enviando imagem para o celular")
                foto = open('/home/pi/Downloads/Imagens/imgTest.jpg',"rb")
                imageString = foto.read()
                byteArray = bytes(imageString)
                publish.single("PetFeeder/foto", byteArray, hostname='iot.eclipse.org')
                globals.eventoEnviarImg.clear()
                
            time.sleep(2)
            


import threading
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
import datetime
import globals

class Mqtt(threading.Thread):

    def on_connect(self, client, userdata, flags, rc):
        print("Conectado ao Broker. Resultado de conexao: " + str(rc))

        # faz subscribe para receber msgs
        client.subscribe("TccUtfFinal")

    def on_message(self, client, userdata, msg):

        #Recebeu nova hora de servir (72 = H)
        if msg.payload[0] == 72:
            #Escreve a hora recebida (-48 eh pq o valor ta em ASCII)
            hora = (msg.payload[1] - 48) * 10 + (msg.payload[2] - 48)
            minuto = (msg.payload[3] - 48) * 10 + (msg.payload[4] - 48)
            with globals.mutexHora:
                globals.horaAlimentar = datetime.time(hora, minuto)
                print("Nova hora de servir: " + str(globals.horaAlimentar))


    def thread_mqtt(self):
        # inicializa MQTT:
        client = mqtt.Client('RaspberryClient')
        client.on_connect = self.on_connect
        client.on_message = self.on_message

        client.connect("iot.eclipse.org", 1883, 60)

        print('Thread mqtt iniciada')

        client.loop_forever()


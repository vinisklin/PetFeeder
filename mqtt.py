import threading
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish

class Mqtt(threading.Thread):

    def on_connect(self, client, userdata, flags, rc):
        print("Conectado ao Broker. Resultado de conexao: " + str(rc))

        # faz subscribe para receber msgs
        client.subscribe("TccUtfFinal")

    def on_message(self, client, userdata, msg):
        print('Recebeu msg')

        if msg.payload == "Hello":
            pass

    def thread_mqtt(self):
        # inicializa MQTT:
        client = mqtt.Client('RaspberryClient')
        client.on_connect = self.on_connect
        client.on_message = self.on_message

        client.connect("iot.eclipse.org", 1883, 60)

        print('Thread mqtt iniciada')

        client.loop_forever()


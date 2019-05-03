import threading
import mqtt
import relogio_botao as rb
import camera_ia as cam
import servo
import strain_gage as sg
import datetime
import globals

#------------------MAIN----------------------
if __name__ == "__main__":
    #Le variaveis salvas em arquivo para inicializacao
    file = open('/home/pi/Downloads/Imagens/memory.txt','r')
    porcao = int(file.readline())
    h = int(file.readline())
    m = int(file.readline())
    file.close()
    
    #Inicializa as variaveis globais
    globals.eventoAlimentar = threading.Event()
    globals.eventoEnviarImg = threading.Event()
    globals.eventoPorcaoServida = threading.Event()

    globals.pesoPorcao = porcao 
##    globals.horaAlimentar = datetime.time(h, m)
    globals.horaAlimentar = datetime.time(19, 46) #Apenas para testar
    print(globals.horaAlimentar)

    globals.mutexHora = threading.Lock()

    #Instancia as classes
    c_mqtt = mqtt.Mqtt()
    c_relogioBotao = rb.Relogio_botao()
    c_cameraIA = cam.Camera_ia()
    c_servo = servo.Servo()
    c_strainG = sg.Strain_gage()

    #Define e inicializa as threads que ficarao rodando sempre
    t_mqtt          = threading.Thread(target=c_mqtt.thread_mqtt, name='mqtt')
    t_relogioBotao  = threading.Thread(target=c_relogioBotao.thread_relogio_botao, name = 'relogio_botao')
    t_cameraIA = threading.Thread(target=c_cameraIA.thread_camera_ia, name='camera_ia')

    t_mqtt.start()
    t_relogioBotao.start()
    t_cameraIA.start()

    #Aguarda o momento de liberar a racao
    while True:
        # Espera alguem pedir para liberar a racao
        globals.eventoAlimentar.wait()

        # Cria as threads necessarias p liberar a racao
        t_servo = threading.Thread(target=c_servo.thread_servo, name='servo')
        t_strainGage = threading.Thread(target=c_strainG.thread_strain_gage, name='strain_gage')


        t_servo.start()
        t_strainGage.start()

        #Main espera o final das threads
        t_servo.join()
        t_strainGage.join()

        globals.eventoAlimentar.clear()


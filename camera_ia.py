import threading
from keras.models import load_model
from keras.preprocessing import image
from picamera import PiCamera
import time
import matplotlib.pyplot as plt
import numpy as np
import globals

img_path = '/home/pi/Downloads/Imagens/imgTest.jpg'
camera = PiCamera()

class Camera_ia(threading.Thread):
    
    def thread_camera_ia(self):
        print('Thread camera iniciada')
        
        
        model = load_model("seventh_try.h5")
        print('Modelo carregado')

        while True:
            # So executa se a porcao ja estiver sido servida
            globals.eventoPorcaoServida.wait()

            poteCheio = True
            
            while poteCheio:

                camera.resolution = (1280, 720)
                camera.start_preview()
                camera.brightness = 60
                time.sleep(1)
                camera.capture(img_path, resize=(500,281))
                camera.stop_preview()

                img = image.load_img(img_path, target_size=(150, 150))
                img_tensor = image.img_to_array(img)                    # (height, width, channels)
                img_tensor = np.expand_dims(img_tensor, axis=0)         # (1, height, width, channels), add a dimension because the model expects this shape: (batch_size, height, width, channels)
                img_tensor /= 255.
                
                pred = model.predict(img_tensor)
                print(pred)
                
                if pred[0][0] >= 0.8: 
                    print('I am {:.2%} sure this is empty'.format(pred[0][0]))
                    poteCheio = False
                    globals.eventoNotificarPoteVazio.set()
                    
                time.sleep(5)
                
            globals.eventoPorcaoServida.clear()

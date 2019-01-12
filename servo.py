import threading
# import RPi.GPIO as GPIO

class Servo(threading.Thread):

    def thread_servo(self):
        print('Thread servo iniciada')
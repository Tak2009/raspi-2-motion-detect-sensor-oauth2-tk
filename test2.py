from multiprocessing import Process
import time
import RPi.GPIO as GPIO

def f(name):
    print('In the fucntion')
    time.sleep(6)
    print('After sleep')
    print('hello', name)
    
def m():
    return "Hello, TK"

p = Process(target=f, args=('bob',))
p.start()
time.sleep(4)
#p.kill()
print("Proces killed")

GPIO.cleanup()

import RPi.GPIO as GPIO
import time
import datetime
from picamera import PiCamera
import os

PIR_PIN = 4
LED_PIN = 17
LOG_FILE_NAME = "/home/pi/Python/Project_2/static/photo/photo_logs.txt"

def take_photo(camera):
    file_name = "/home/pi/Python/Project_2/static/photo/img_" + datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + ".jpg"
    camera.capture(file_name)
    return file_name

def update_photo_log_file(photo_file_name):
    with open(LOG_FILE_NAME, "a") as f:
        f.write(photo_file_name)
        f.write("\n")
                        
# setup a camera
camera = PiCamera()
camera.resolution = (720, 480)
camera.rotation = 180
print("Waiting 2 seconds to ini the camera now..")
time.sleep(2)
print("Camera setup done")

# remove log file
if os.path.exists(LOG_FILE_NAME):
    os.remove(LOG_FILE_NAME)
    print("Log file removed")
    
# setup GPIOs for sensor and led
GPIO.setmode(GPIO.BCM)
GPIO.setup(PIR_PIN, GPIO.IN)
GPIO.setup(LED_PIN, GPIO.OUT)
GPIO.output(LED_PIN, GPIO.LOW)
print("GPIOs set-up")

MOVE_DETECT_TRESHOLD = 3.0
pir_state = GPIO.input(PIR_PIN)
last_pir_state = GPIO.input(PIR_PIN)
movement_timer = time.time()
MIN_DURATION_BETWEEN_2_PHOTOS = 10.0
last_time_photo_taken = 0

print("Everything has been setup")

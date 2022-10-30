import RPi.GPIO as GPIO
import time
import datetime
from picamera import PiCamera
import os
import send_gmail

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
last_pir_state = GPIO.input(PIR_PIN)
movement_timer = time.time()
MIN_DURATION_BETWEEN_2_PHOTOS = 10.0
last_time_photo_taken = 0

print("Everything has been setup")

try:
    while True:
        time.sleep(0.01)
        pir_state = GPIO.input(PIR_PIN)
        if pir_state == GPIO.HIGH:
            GPIO.output(LED_PIN, GPIO.HIGH)
        else:
            GPIO.output(LED_PIN, GPIO.LOW)
        if last_pir_state == GPIO.LOW and pir_state == GPIO.HIGH:
            movement_timer = time.time()
        if last_pir_state == GPIO.HIGH and pir_state == GPIO.HIGH:
            if time.time() - movement_timer > MOVE_DETECT_TRESHOLD:
                if time.time() - last_time_photo_taken > MIN_DURATION_BETWEEN_2_PHOTOS:
                    print("Take a photo and send it by email")
                    photo_file_name = take_photo(camera)
                    update_photo_log_file(photo_file_name)
                    send_gmail.mainProcess(photo_file_name)
                    print("Email sent")
                    last_time_photo_taken = time.time()
        last_pir_state = pir_state
except KeyboardInterrupt:
    GPIO.cleanup()
    print(" : interrupt by Ctr + C")
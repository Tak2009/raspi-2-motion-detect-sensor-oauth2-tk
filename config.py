import RPi.GPIO as GPIO
import time
import datetime
from picamera import PiCamera
import os
import send_gmail as Gmail

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

def take_photo_now():
    global last_pir_state
    global last_time_photo_taken
    global pir_state
    pir_state = GPIO.input(PIR_PIN)
    print("Take a photo now")
    photo_file_name = take_photo(camera)
    update_photo_log_file(photo_file_name)
    print("Photo taken. Check http://0.0.0.0:5000/check-movement")
    last_time_photo_taken = time.time()
    last_pir_state = pir_state
    message = "http://0.0.0.0:5000/check-movement"
    return message
        
def auto_switch(on_off_flag):
    global auto_flag
    if on_off_flag == "off":
        if auto_flag == "on":
            auto_flag = "off"
            return "Auto turned off now"
        else:
            return "Auto off already"
    if on_off_flag == "on":
        if auto_flag == "off":
            auto_flag = "on"
            return "Auto turned on now"
        else:
            return "Auto on already"
    return "Please set \"on\" or \"off\""

def take_photo_automatically():
    global last_pir_state
    global movement_timer
    global last_time_photo_taken
    global pir_state
    print("Auto job is now running")
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
                    print('CheckOn5: ' + str(type(camera)))
                    photo_file_name = take_photo(camera)
                    update_photo_log_file(photo_file_name)
                    Gmail.gmailSender(photo_file_name)
                    print("Photo taken and email sent out")
                    last_time_photo_taken = time.time()
        last_pir_state = pir_state

def test():
    print('testing the scheduler. this will terminate 15 sec later!: ' + str(datetime.datetime.now().hour) + '-' + str(datetime.datetime.now().minute))
    time.sleep(10)
    print('test finished')

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

auto_flag = "off"

print("Everything has been setup")




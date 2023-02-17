import RPi.GPIO as GPIO
import time
import datetime
from picamera import PiCamera
import os
import send_gmail as gmail
import network as n
import apis as api

PROJECT_FOLDER = "/home/pi/Python/raspi-2-motion-detect-sensor-oauth2-tk"
LOG_FILE_NAME = PROJECT_FOLDER + '/static/photo/photo_logs.txt'

pir_pin = 4
led_pin = 17
move_detect_threshold = 3.0
pir_state = ""
last_pir_state = ""
movement_timer = time.time()
min_duration_bw_2_photos = 60.0
last_time_photo_taken = 0
auto_flag = "off"

def set_gpio():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(pir_pin, GPIO.IN)
    GPIO.setup(led_pin, GPIO.OUT)
    GPIO.output(led_pin, GPIO.LOW)
    print("GPIOs set-up")
    
def clean_gpio():
    print('Mode Check Before Cleanup: ' + str(type(GPIO.getmode())))
    GPIO.cleanup()
    print('Mode Check After Cleanup: ' + str(GPIO.getmode()))

def take_photo(camera):
    file_name = PROJECT_FOLDER + "/static/photo/img_" + datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + ".jpg"
    camera.capture(file_name)
    return file_name

def update_photo_log_file(photo_file_name):
    with open(LOG_FILE_NAME, "a") as f:
        f.write(photo_file_name)
        f.write("\n")
        
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

def take_photo_now():
    if not isinstance(GPIO.getmode(), int):
        set_gpio()
    global last_pir_state
    global last_time_photo_taken
    global pir_state
    pir_state = GPIO.input(pir_pin)
    print("Take a photo now")
    photo_file_name = take_photo(camera)
    update_photo_log_file(photo_file_name)
    print("Photo taken and email sent out")
    url = api.asyncio.run(api.main())
    gmail.gmailSender(photo_file_name, url)
    last_time_photo_taken = time.time()
    last_pir_state = pir_state
    clean_gpio()
    message = [f'http://{n.HOST}:{n.PORT}/check-movement', f'http://{n.HOST}:{n.PORT}/check-movement-2']
    print(str(message))
    return message

def take_photo_automatically(event):
    # check if GPIO.setmode(GPIO.BCM) = 11
    if not isinstance(GPIO.getmode(), int):
        set_gpio()
    global last_pir_state
    global movement_timer
    global last_time_photo_taken
    global pir_state
    global pir_pin
    global led_pin
    global move_detect_threshold
    global min_duration_bw_2_photos
    last_pir_state = GPIO.input(pir_pin)
    print("Auto job will be running in 2 sec")
    time.sleep(2)
    while True:
        time.sleep(0.01)
        pir_state = GPIO.input(pir_pin)
        if pir_state == GPIO.HIGH:
            GPIO.output(led_pin, GPIO.HIGH)
        else:
            GPIO.output(led_pin, GPIO.LOW)
        if last_pir_state == GPIO.LOW and pir_state == GPIO.HIGH:
            movement_timer = time.time()
        if last_pir_state == GPIO.HIGH and pir_state == GPIO.HIGH:
            if time.time() - movement_timer > move_detect_threshold:
                if time.time() - last_time_photo_taken > min_duration_bw_2_photos:
                    print("Take a photo and send it by email")
                    photo_file_name = take_photo(camera)
                    update_photo_log_file(photo_file_name)
                    url = api.asyncio.run(api.main())
                    gmail.gmailSender(photo_file_name, url)
                    print("Photo taken and email sent out")
                    last_time_photo_taken = time.time()
        last_pir_state = pir_state
        if event.is_set():
            clean_gpio()
            break
    print('Exited from the auto while loop function')

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
set_gpio()

print("Everything has been setup")




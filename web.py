from flask import Flask, render_template, redirect
from jinja2 import Template
import os
import config as c
import network as n
import datetime
import time
from threading import Thread
# https://superfastpython.com/stop-a-thread-in-python/#Stop_Custom_Function_in_New_Thread
# https://blog.miguelgrinberg.com/post/how-to-kill-a-python-thread
# https://docs.python.org/3/library/threading.html#event-objects
from threading import Event

FOLDER_PATH = "/home/pi/Python/raspi-2-motion-detect-sensor-oauth2-tk/static"
LOG_FILE_NAME = FOLDER_PATH + "/photo/photo_logs.txt"
cumulative_photo_counter = 0

# initialize a thread for while loop
thread = ""
event = Event()

# flask-divice
web_app = Flask(__name__, static_url_path=FOLDER_PATH, static_folder=FOLDER_PATH)

host_port = f'{n.HOST}:{n.PORT}'

@web_app.route("/")
def index ():
    mode = c.auto_flag
    return render_template("index.html", mode=mode, host_port=host_port)
    
@web_app.route("/check-movement")
def check_movement():
    message = ""
    line_counter = 0
    last_photo_file_name = 0
    if os.path.exists(LOG_FILE_NAME):
        with open(LOG_FILE_NAME,"r") as f:
            for line in f:
                line_counter += 1
                last_photo_file_name = line
        global cumulative_photo_counter
        difference_since_last_time = line_counter -  cumulative_photo_counter
        if difference_since_last_time == 1:
            message = str(difference_since_last_time) + " photo was taken since the last check. <br/><br/>"
        else:
            message = str(difference_since_last_time) + " photos were taken since the last check. <br/><br/>"
        message += "Last photo: " + last_photo_file_name + "<br/>"
        message += "<img src=\"" + last_photo_file_name + "\"><br/>"
        cumulative_photo_counter = line_counter 
    else:
        message = "Nothing new<br/>"
    message += f'<p>Go back to <a href=\"http://{n.HOST}:{n.PORT}\">/index</a></p>'
    return message

@web_app.route("/check-movement-2")
def check_movement_2():
    message = ""
    line_counter = 0
    last_photo_file_name = 0
    if os.path.exists(LOG_FILE_NAME):
        with open(LOG_FILE_NAME,"r") as f:
            for line in f:
                line_counter += 1
                last_photo_file_name = line
        global cumulative_photo_counter
        difference_since_last_time = line_counter -  cumulative_photo_counter
        print(str(difference_since_last_time))
        cumulative_photo_counter = line_counter
        print(str(difference_since_last_time))
        return render_template("check-movement.html", number=difference_since_last_time, file_name=last_photo_file_name, host_port=host_port)
    else:
        return render_template("check-movement.html", number=0, host_port=host_port)

@web_app.route("/auto-mode/<on_off_flag>")
def auto_on_off(on_off_flag):
    global thread
    global event
    # Reset the internal flag to false. This is necessary to "reset" the event after set() was called previously. 
    event.clear()
    print(type(thread))
    c.auto_switch(on_off_flag)
    if on_off_flag == "on":
        if isinstance(thread, str):
            print('CheckOn1: ' + on_off_flag)
            print('CheckOn2: ' + str(type(thread)))
            thread = Thread(target=c.take_photo_automatically, args=(event,))
            date = datetime.datetime.now()
            thread.start()
            print('A thread started for the ahto while loop mode: ' + str(date.hour) + '-' + str(date.minute) )
            print('CheckOn3: ' + str(type(thread)))
        else:
            print('The thread for the auto while loop mode exists; the auto-mode has been on')
    if on_off_flag == "off":
        if not isinstance(thread, str):
            print('CheckOff1: ' + on_off_flag)
            print('CheckOff2: ' + str(type(thread)))
            event.set()
            print('Event thrown to the thread for the auto while loop mode to force the thread to stop')
            print('Auto mode turned off now')
            thread = ""
            print('CheckOff3: ' + str(type(thread)))
        else:
            print('No thread for the auto while loop mode exists; the auto-mode has been already off')
            print('CheckOff4: '+ str(type(thread)))
    print('Before redirect')
    return redirect(f'http://{n.HOST}:{n.PORT}')

@web_app.route("/take-photo-now")
def take_photo_manually():
    message = c.take_photo_now()
    return render_template("take-photo-now.html", message=message, host_port=host_port)

web_app.run(host=n.HOST, port=n.PORT)



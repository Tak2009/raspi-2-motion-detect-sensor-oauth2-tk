from flask import Flask, render_template, redirect
import os
import config as Conf

import datetime
from time import sleep
from threading import Thread

FOLDER_PATH = "/home/pi/Python/Project_2/static"
LOG_FILE_NAME = FOLDER_PATH + "/photo/photo_logs.txt"
cumulative_photo_counter = 0

# initialize a thread for while loop
thread = ""

def test():
    print('testing the scheduler. this will terminate 15 sec later!: ' + str(datetime.datetime.now().hour) + '-' + str(datetime.datetime.now().minute))
    sleep(15)
    print('test finished')

web_app = Flask(__name__, static_url_path=FOLDER_PATH, static_folder=FOLDER_PATH)

@web_app.route("/")
def index ():
    mode = Conf.auto_flag
    return render_template("index.html", mode=mode)
    
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
        message = str(difference_since_last_time) + " photo(s) were taken since the last check. <br/><br/>"
        message += "Last photo: " + last_photo_file_name + "<br/>"
        message += "<img src=\"" + last_photo_file_name + "\">"
        cumulative_photo_counter = line_counter 
    else:
        message = "Nothing new"
    return message

@web_app.route("/check-time-stamp")
def time_stamp ():
    return render_template("check-time-stamp.html")

@web_app.route("/auto-mode/<on_off_flag>")
def auto_on_off(on_off_flag):
    global thread
    print(type(thread))
    Conf.auto_switch(on_off_flag)
    if on_off_flag == "on":
        if isinstance(thread, str):
            print('CheckOn1: ' + on_off_flag)
            print('CheckOn2: ' + str(type(thread)))
            thread = Thread(target=test)
            date = datetime.datetime.now()
            sched.start()
            print('Thread set up and a job' + str(date.hour) + '-' + str(date.minute) )
            print('CheckOn3: ')
            print('CheckOn4: ' + str(type(thread)))
        else:
            print('BackgroundScheduler exists and \'auto\' job is running in the backgroundand: the auto-mode is already on')
    if on_off_flag == "off":
        if not isinstance(thread, str):
            print('CheckOff1: ' + on_off_flag)
            print('CheckOff2: ' + str(type(thread)))
            sched.shutdown(wait=False)
            print('Thread shut down')
            print('Auto job is now off')
            thread = ""
            print('CheckOff3: ' + str(type(sched)))
        else:
            print('No BackgroundScheduler exists and the auto-mode is already off')
            print('CheckOff4: '+ str(type(sched)))
    print('Check5: all ifs done')  
    return redirect('http://0.0.0.0:5000')

@web_app.route("/take-photo-now")
def take_photo_manually():
    message = Conf.take_photo_now()
    return render_template("take-photo-now.html", message=message)

web_app.run(host="0.0.0.0")



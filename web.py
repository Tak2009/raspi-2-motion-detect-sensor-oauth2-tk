from flask import Flask, render_template, redirect
import os
import config as Conf

FOLDER_PATH = "/home/pi/Python/Project_2/static"
LOG_FILE_NAME = FOLDER_PATH + "/photo/photo_logs.txt"
cumulative_photo_counter = 0

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
    Conf.auto_switch(on_off_flag)
    Conf.take_photo_automatically()
    print('Check: ' + Conf.auto_flag)
    return redirect('http://0.0.0.0:5000')

@web_app.route("/take-photo-now")
def take_photo_manually():
    message = Conf.take_photo_now()
    return render_template("take-photo-now.html", message=message)

web_app.run(host="0.0.0.0")



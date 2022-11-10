# https://flask.palletsprojects.com/en/2.2.x/async-await/
# https://flask.palletsprojects.com/en/2.0.x/changes/#version-2-0-2
# https://testdriven.io/blog/flask-async/
# get Flask2.0 or above = $pip install -U Flask
# then $pip install flask[async]
from flask import Flask, render_template, redirect
import os
import config as Conf
import asyncio

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
    if Conf.auto_flag == "on":
        Conf.take_photo_automatically()
        print('Check: ' + Conf.auto_flag)
    if Conf.auto_flag == "off":
        print('Check: ' + Conf.auto_flag)
    return redirect('http://0.0.0.0:5000')

# @web_app.route("/auto-mode/<on_off_flag>")
# async def auto_on_off(on_off_flag):
#     Conf.auto_switch(on_off_flag)
#     print('Check1: ' + Conf.auto_flag)
#     if Conf.auto_flag == "off":
#         print('Check2: ' + Conf.auto_flag)
#         return redirect('http://0.0.0.0:5000')
#     if Conf.auto_flag == "on":
#         task_1 = asyncio.create_task(Conf.async_take_photo_automatically())
#         task_1 = asyncio.create_task(Conf.async_test_1())
#         task_2 = asyncio.create_task(Conf.async_test_2())
#         task_3 = asyncio.create_task(Conf.async_test_3())
#         await task_1
#         await task_2
#         await task_3
#         print('Check3: ' + Conf.auto_flag)
#         return redirect('http://0.0.0.0:5000')

@web_app.route("/take-photo-now")
def take_photo_manually():
    message = Conf.take_photo_now()
    return render_template("take-photo-now.html", message=message)

web_app.run(host="0.0.0.0")



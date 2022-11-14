from flask import Flask, render_template, redirect
import os
import config as Conf
# https://apscheduler.readthedocs.io/en/latest/
# https://www.pytry3g.com/entry/apscheduler#%E3%82%B5%E3%83%B3%E3%83%97%E3%83%AB%EF%BC%91%EF%BC%93%EF%BC%91%EF%BC%99%E6%99%82%EF%BC%94%EF%BC%90%E5%88%86%E3%81%AB%E6%8C%87%E5%AE%9A%E3%81%97%E3%81%9F%E3%83%97%E3%83%AD%E3%82%B0%E3%83%A9%E3%83%A0%E3%81%AE%E8%87%AA%E5%8B%95%E5%AE%9F%E8%A1%8C
# https://apscheduler.readthedocs.io/en/3.x/modules/triggers/date.html
from apscheduler.schedulers.background import BackgroundScheduler
import datetime

FOLDER_PATH = "/home/pi/Python/Project_2/static"
LOG_FILE_NAME = FOLDER_PATH + "/photo/photo_logs.txt"
cumulative_photo_counter = 0

# initialize a sheduler
sched = ""

def test():
    print('testing the scheduler. this was set 1 min ago!: ' + str(datetime.datetime.now().hour) + '-' + str(datetime.datetime.now().minute))

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
    global sched
    global executors
    print(type(sched))
    Conf.auto_switch(on_off_flag)
    if on_off_flag == "on":
        if isinstance(sched, str):
            print('CheckOn1: ' + on_off_flag)
            print('CheckOn2: ' + str(type(sched)))
            sched = BackgroundScheduler()
            date = datetime.datetime.now()
            sched.add_job(Conf.take_photo_automatically, 'date', run_date=datetime.datetime(date.year, date.month, date.day, date.hour, date.minute + 1, date.second), id='auto')
            sched.start()
            print('BackgroundScheduler set up and a job has been scheduled. The job, \'auto\' will start running in 1 min: ' + str(date.hour) + '-' + str(date.minute) )
            print('CheckOn3: '+ str(sched.get_jobs()))
            print('CheckOn4: ' + str(type(sched)))
        else:
            print('BackgroundScheduler exists and \'auto\' job is running in the backgroundand: the auto-mode is already on')
    if on_off_flag == "off":
        if not isinstance(sched, str):
            print('CheckOff1: ' + on_off_flag)
            print('CheckOff2: ' + str(type(sched)))
            sched.shutdown(wait=False)
            print('BackgroundScheduler shut down')
            print('Auto job is now off')
            sched = ""
            executor = ""
            print('CheckOff3: ' + str(type(sched)))
        else:
            print('No BackgroundScheduler exists and the auto-mode is already off')
            print('CheckOff4: '+ str(type(sched)))
    return redirect('http://0.0.0.0:5000')

@web_app.route("/take-photo-now")
def take_photo_manually():
    message = Conf.take_photo_now()
    return render_template("take-photo-now.html", message=message)

web_app.run(host="0.0.0.0")



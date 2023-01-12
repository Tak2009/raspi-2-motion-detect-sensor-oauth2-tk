# raspi-2-motion-detect-sensor-oauth2-tk

Developed as a first IoT project when my house suffered from mice attack on the stored food in our garage. Connected with Gmail via Oauth 2.0. Via the web app, we can check the log file and the latest photo taken as well as change the mode: motion detect auto mode and manual camera mode. 

* GPIO programming using Python 3 on Raspberry Pi 4
* 1 Raspberry Pi, 1 PIR sensor and 1 Night vision Pi camera are used
* Gmail notification email with photo attached when motion is detected. OAuth 2.0 is used for higher security to connect Gmail with this app
* Flask for a simple but a bit amusing web app to control the camera device(auto and manual mode), check the logs and see the most recent photo upon request. Multi-thread is used. Flask-Jinja template and JavaScript. Python threading library and simple async await used in JavaScript.

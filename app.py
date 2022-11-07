import config as Conf
import send_gmail as Gmail

try:
    while True:
        Conf.time.sleep(0.01)
        Conf.pir_state = Conf.GPIO.input(Conf.PIR_PIN)
        if Conf.pir_state == Conf.GPIO.HIGH:
            Conf.GPIO.output(Conf.LED_PIN, Conf.GPIO.HIGH)
        else:
            Conf.GPIO.output(Conf.LED_PIN, Conf.GPIO.LOW)
        if Conf.last_pir_state == Conf.GPIO.LOW and Conf.pir_state == Conf.GPIO.HIGH:
            Conf.movement_timer = Conf.time.time()
        if Conf.last_pir_state == Conf.GPIO.HIGH and Conf.pir_state == Conf.GPIO.HIGH:
            if Conf.time.time() - Conf.movement_timer > Conf.MOVE_DETECT_TRESHOLD:
                if Conf.time.time() - Conf.last_time_photo_taken > Conf.MIN_DURATION_BETWEEN_2_PHOTOS:
                    print("Take a photo and send it by email")
                    photo_file_name = Conf.take_photo(Conf.camera)
                    Conf.update_photo_log_file(photo_file_name)
                    Gmail.gmailSender(photo_file_name)
                    print("Photo taken and email sent out")
                    Conf.last_time_photo_taken = Conf.time.time()
        Conf.last_pir_state = Conf.pir_state
except KeyboardInterrupt:
    Conf.GPIO.cleanup()
    print(" : interrupt by Ctr + C")
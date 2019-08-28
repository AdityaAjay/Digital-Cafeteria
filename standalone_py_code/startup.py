import RPi.GPIO as GPIO
import time
import os

GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP)


def start(channel):
    os.system("python3 welcome.py")


GPIO.add_event_detect(18, GPIO.FALLING, callback=start, bouncetime=2000)
while 1:
    time.sleep(5)

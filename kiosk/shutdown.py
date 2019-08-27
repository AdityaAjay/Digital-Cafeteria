#!/usr/bin/env python3
# to execute at startup
import RPi.GPIO as GPIO
import time
import os

GPIO.setmode(GPIO.BCM)
GPIO.setup(26, GPIO.IN, pull_up_down=GPIO.PUD_UP)


def Shutdown(channel):
    os.system("sudo shutdown -h now")


GPIO.add_event_detect(26, GPIO.FALLING, callback=Shutdown, bouncetime=2000)

while 1:
    time.sleep(5)

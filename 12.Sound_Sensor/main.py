# -*- coding:utf-8 -*-
#!/usr/bin/python
#Author: Dharmendra Kumar Yadav
#######################################################

import RPi.GPIO as GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

GPIO.setup(17, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
GPIO.setup(4, GPIO.OUT, initial = GPIO.LOW)

while True:
    sensor = GPIO.input(17)
    if sensor == 0:
        print("No sound!")
        GPIO.output(4, 0)
    elif sensor == 1:
        print("Sound detected!")
        GPIO.output(4, 1)

# -*- coding:utf-8 -*-
#!/usr/bin/python
#Author: Dharmendra Kumar Yadav
#######################################################

import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

GPIO.setup(27, GPIO.OUT)

hz = input('Please define the Switch PWM frequency in Hertz(recommended:75): ')
dc = input('Please define the Switch PWM Duty Cycle: ')

switch = GPIO.PWM(27, hz)

try:
    while True:
        switch.start((dc / 2.55))

except KeyboardInterrupt:
    switch.stop()
    GPIO.cleanup()

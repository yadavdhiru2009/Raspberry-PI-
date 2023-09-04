# -*- coding:utf-8 -*-
#!/usr/bin/python
#Author: Dharmendra Kumar Yadav
#######################################################
from gpiozero import Button

button = Button(18)

while True:
    if button.is_pressed:
        print("Button is pressed")
    else:
        print("Button is not pressed")

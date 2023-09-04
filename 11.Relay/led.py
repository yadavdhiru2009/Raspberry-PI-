# -*- coding:utf-8 -*-
#!/usr/bin/python
#Author: Dharmendra Kumar Yadav
#######################################################
from gpiozero import Relay
from time import sleep

Relay = Relay(17)

while True:
    Relay.on()
    sleep(1)
    Relay.off()
    sleep(1)

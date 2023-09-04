# -*- coding:utf-8 -*-
#!/usr/bin/python
#Author: Dharmendra Kumar Yadav
#######################################################

import smbus
import time

address = 0x48
A0 = 0x40
A1 = 0x41
A2 = 0x42
A3 = 0x43
bus = smbus.SMBus(1)
while True:
    bus.write_byte(address,A0)
    value = bus.read_byte(address)
    print("AOUT:%1.3f  " %(value*3.3/255))
    time.sleep(0.1)

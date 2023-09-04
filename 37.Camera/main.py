# -*- coding:utf-8 -*-
#!/usr/bin/python
#Author: Dharmendra Kumar Yadav
#######################################################

import picamera
import time

camera = picamera.PiCamera()
camera.capture('example.jpg')

camera.vflip = True

camera.capture('example2.jpg')

camera.start_recording('examplevid.h264')
time.sleep(5)
camera.stop_recording()

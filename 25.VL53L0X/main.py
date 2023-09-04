# -*- coding:utf-8 -*-
#!/usr/bin/python
#Author: Dharmendra Kumar Yadav
#######################################################


import VL53L1X #sudo pip3 install vl53l1x
import time

tof = VL53L1X.VL53L1X(i2c_bus=1, i2c_address=0x29)
print("Python: Initialized")
tof.open()
print("Python: Opened")


time_start = time.time()

try :
    while True:


        ### ------------------- get_time ----------------- ###

        time_end = time.time()
        time_elapsed = time_end - time_start

        print("")
        print("--- Time : {:.1f}s ---".format(time_elapsed))

        ### ------------------- get_distance ----------------- ###

        ### --- Short Range --- ###
        tof.start_ranging(1)    # 1 = Short Range
        distance_mm = tof.get_distance()
        print("Short Range Distance: {}mm".format(distance_mm))
        tof.stop_ranging()

        ### --- Medium Range --- ###
        tof.start_ranging(2)    # 2 = Medium Range
        distance_mm = tof.get_distance()
        print("Medium Range Distance: {}mm".format(distance_mm))
        tof.stop_ranging()

        ### --- Long Range --- ###
        tof.start_ranging(3)    # 3 = Long Range
        distance_mm = tof.get_distance()
        print("Long Range Distance: {}mm".format(distance_mm))
        tof.stop_ranging()


        time.sleep(1)

except KeyboardInterrupt:
        print("\nCtrl+C")

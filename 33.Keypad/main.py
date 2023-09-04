# -*- coding:utf-8 -*-
#!/usr/bin/python
#Author: Dharmendra Kumar Yadav
#######################################################

import sys
import time

import Adafruit_MPR121.MPR121 as MPR121

cap = MPR121.MPR121()

if not cap.begin():
    sys.exit(1)

keypads = {3:1, 7:2, 11:3, 2:4, 6:5, 10:6, 1:7, 5:8, 9:9, 0:'*', 4:0, 8:'#'}
def main():
    last_touched = cap.touched()
    while True:
        current_touched = cap.touched()
        for i in range(12):
            pin_bit = 1 << i
            if current_touched & pin_bit and not last_touched & pin_bit:
                for real, wanted in keypads.iteritems():
		    if real == i:
			print wanted
        last_touched = current_touched
        time.sleep(0.1)

if __name__=="__main__":
    main()

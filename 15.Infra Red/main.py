# -*- coding:utf-8 -*-
#!/usr/bin/python
#Author: Dharmendra Kumar Yadav
#######################################################

import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)

def my_callback(channel):
        global i        
        i = i+1
        
def main():
        

        GPIO.setup(27, GPIO.OUT)
        GPIO.setup(17, GPIO.IN)

        led = GPIO.PWM(27, 100)

        GPIO.add_event_detect(17, GPIO.BOTH, callback=my_callback)
        try:
                global i

                i = 0
                led.start(50)
                while True:
                        if i <= 17:
                                print ('Signal')                                
                        i = 0                
                        time.sleep(0.1)                                

        except KeyboardInterrupt:
                led.stop()   
                GPIO.cleanup()
if __name__ == "__main__":
    main()

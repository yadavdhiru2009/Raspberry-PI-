# -*- coding:utf-8 -*-
#!/usr/bin/python
#Author: Dharmendra Kumar Yadav
#######################################################
from gpiozero import LEDCharDisplay
#import the LEDCharDisplay library from gpiozero
from time import sleep
#import the sleep library from time

display = LEDCharDisplay(26, 19, 13, 6, 5, 21, 20, active_high=False)
#declared the GPIO pins for (a,b,c,d,e,f,g) and declared its CAS

while True:
#initialize the infinite while loop

     for char in '0123456789':
     #initialize for loop and store 0123456789 in variable char

         display.value = char
         #displayed the value

         sleep(1)
         #generated delay of one second

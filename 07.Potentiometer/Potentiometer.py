# -*- coding:utf-8 -*-
#!/usr/bin/python
#Author: Dharmendra Kumar Yadav
#######################################################
from gpiozero import MCP3008

pot = MCP3008(channel=0)

while True:
    print(pot.value)

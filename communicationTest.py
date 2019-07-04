# -*- coding: utf-8 -*-
"""
Created on Mon Jul  1 17:47:33 2019

@author: ROBERTO MARIO
"""

import serial
import RPi.GPIO as GPIO
import time

ser=serial.Serial("/dev/ttyACM0",9600)  #change ACM number as found from ls /dev/tty/ACM*
ser.baudrate=9600

time.sleep(5)

def tell(msg):
    msg = msg + '\n'
    x = msg.encode('ascii') # encode n send
    ser.write(x)

tell('w50')
time.sleep(5)
tell('e')
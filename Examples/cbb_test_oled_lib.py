#cbb_test_oled_driver.py
#
# Copyright (C) 2024 KW Services.
# MIT License
# MicroPython 1.20
#
from pyb import Pin
from machine import I2C
import time
import random
#import math
#import array

##### flash drive ################
# driver file: ssd1306.py must be on flash drive of BlackPill
import ssd1306
# lib file: cbb_oled_lib.py must be on flash drive of BlackPill
from cbb_oled_lib import drawBarChartV, drawBarChartH, drawDial
# fonts are 8 pixels high, so 8 lines (16 pixels)
# OLED has Yellow title 2-line area and below a Blue 6-line area (48 pixels)
# center is 40,40 in the blue area
# max radius is 24 pixels in blue

### Constants and PIN Definitions ###############
# Parameter setting of screen characteristics in Pixels
oled_screen_width = 128
oled_screen_length = 64
BLACK = 0
WHITE = 1
# Define the Pins for the 4-socket hearder label I2C1 Port.
SCL_PIN = 'PB6'
SDA_PIN = 'PB7'


### Setup #########################
# Initialization of the I2C1 device
i2c = I2C(scl=Pin(SCL_PIN), sda=Pin(SDA_PIN), freq=100000)
oled = ssd1306.SSD1306_I2C(oled_screen_width, oled_screen_length, i2c)
print("* I2C1 is {}.".format(i2c))

### Tests #########################
print("test1: DrawBarChartV")
for i in range(1,33):
    #val = i/10
    #drawBarChartV(oled,val,0,4,1,0,"A1 BITS", True)
    val = random.randint(0,100)
    drawBarChartV(oled,val,0,100,25,0,"A1 BITS", True)
time.sleep(1)

print("test2: DrawBarChartH")
oled.fill(0)
for i in range(0,33):
    #val = i/10
    #drawBarChartH(oled,val,0,4,1,0,"A1 VOLTS", True)
    val = random.randint(0,100)
    drawBarChartH(oled,val,0,100,25,0,"A1 VOLTS", True)
time.sleep(1)

print("test3: DrawDial")
oled.fill(0)
for i in range(0,33):
    #val = i/10
    #drawDial(oled,val,-0.1,4,1,0,200,"A0 BITS/VOLTS",True)
    val = random.randint(0,100)
    drawDial(oled,val,-0.1,100,25,0,200,"A0 BITS/VOLTS",True)
time.sleep(2)


print("Finish")
oled.fill(0)
oled.show()

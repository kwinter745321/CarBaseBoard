# cbb_test_oled.py
#
# Copyright (C) 2024 KW Services.
# MIT License
# MicroPython 1.20
#
from pyb import Pin, ADC
from machine import I2C
import time
import math

import ssd1306
import random
import array

### Constants and PIN Definitions ##############
# Parameter setting of screen characteristics in Pixels
oled_screen_width = 128
oled_screen_length = 64
BLACK = 0
WHITE = 1
# Define the Pins for the 4-socket hearder label I2C1 Port.
SCL_PIN = "PB6"
SDA_PIN = "PB7"

### Setup #########################
# Initialization of the I2C1 device
i2c = I2C(scl=Pin(SCL_PIN), sda=Pin(SDA_PIN), freq=100000)

oled = ssd1306.SSD1306_I2C(oled_screen_width, oled_screen_length, i2c)
print("* I2C1 is {}.".format(i2c))

# Inspired from MicroPython org web site:
# https://docs.micropython.org/en/latest/esp8266/tutorial/ssd1306.html
#

### Tests #########################  
print("Test1")
oled.text("Test1", 0, 0)
oled.text("text", 0, 8)
oled.text("abcdef", 0, 16)
oled.show()
time.sleep(2)

print("Test2")
oled.fill(0)
oled.text("Test2", 0, 0)
oled.text("MP Logo", 0, 8)
oled.fill_rect(0, 16, 32, 32, 1)
oled.fill_rect(2, 18, 28, 28, 0)
oled.vline(9, 24, 22, 1)
oled.vline(16, 18, 22, 1)
oled.vline(23, 24, 22, 1)
oled.fill_rect(26, 40, 2, 4, 1)
oled.text("MicroPython", 40, 16, 1)
oled.text("SSD1306", 40, 28, 1)
oled.text("OLED 128x64", 40, 40, 1)
oled.show()
time.sleep(2)

print("Test3")
oled.fill(0)
oled.text("Test3", 0, 0)
oled.text("Pixel at 0,26", 0, 8)
oled.pixel(0, 26, 1)                 # set pixel at x=0, y=10 to colour=1
oled.show()
time.sleep(2)

print("Test4")
oled.fill(0)
oled.text("Test4", 0, 0)
oled.text("Draw h & vline", 0, 8)
oled.hline(0, 16, 40, 1)               # draw horizontal line x=0, y=8, width=4, colour=1
oled.vline(0, 16, 40, 1)               # draw vertical line x=0, y=8, height=4, colour=1
oled.show()
time.sleep(2)

print("Test5")
oled.fill(0)
oled.text("Test5", 0, 0)
oled.text("Draw rect", 0, 8)
oled.rect(0, 32, 40, 20, 1)        # draw a rectangle outline 10,10 to 117,53, colour=1
oled.show()
time.sleep(2)
 
print("Test6")
oled.text("Test5", 0, 0, BLACK)		#removes previous text on first line
oled.text("Draw rect", 0, 8, BLACK) #remove
oled.show()
oled.text("Test6", 0, 0)
oled.text("Fill rect", 0, 8)
oled.fill_rect(0, 32, 40, 20, 1)   # draw a solid rectangle 10,10 to 117,53, colour=1
oled.show()
time.sleep(2)

print("reset")
oled.invert(0)
oled.fill(0)
oled.show()

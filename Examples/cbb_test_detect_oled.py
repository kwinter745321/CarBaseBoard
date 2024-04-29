# cbb_test_detect_OLED.py
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
##### flash drive ################
# driver file: hcsr04.py must be on flash drive of BlackPill
# ultraSonic device is HC-SR04 (or HC-SR05)
from hcsr04 import HCSR04
from cbb_oled_lib import drawList

### PIN Definitions ###############
# Pin PB10 is dedicated "wired" to the user button.
USER_BUTTON_PIN = 'PB10'
# IR Detect
DETECT_LEFT_PIN = 'PA0'
DETECT_RIGHT_PIN = 'PA1'
# Define the Pins for the 4-socket hearder label I2C1 Port.
SCL_PIN = 'PB6'
SDA_PIN = 'PB7'
# Parameter setting of screen characteristics in Pixels
OLED_WIDTH = 128
OLED_HEIGHT = 64
#Car Base Board expects HCSR05 device which works at 3.3 volt
# connect a 5-pin cable to device
#SONIC_TRIG_PIN = 'PB8'
#SONIC_ECHO_PIN = 'PB9'

#Inland device HCSR04 **************requires five (5) volt line
# Cannot use the Sonic port
# plug 3-pin cable to adjoining three pins and a separate GND cable
SONIC_TRIG_PIN = 'PB8'
SONIC_ECHO_PIN = 'PB9'

### Setup #########################
# Initialization of the I2C1 device
i2c = I2C(scl=Pin(SCL_PIN), sda=Pin(SDA_PIN), freq=100000)
#led = LED(BUILTIN_LED_NUM)
#led.off()
user = Pin(USER_BUTTON_PIN, Pin.IN, Pin.PULL_UP)
detect_left = Pin(DETECT_LEFT_PIN, Pin.IN, Pin.PULL_UP)
detect_right = Pin(DETECT_RIGHT_PIN, Pin.IN, Pin.PULL_UP)
sonic = HCSR04(trigger_pin=SONIC_TRIG_PIN, echo_pin=SONIC_ECHO_PIN,echo_timeout_us=1000000)
time.sleep(0.2)
oled = ssd1306.SSD1306_I2C(OLED_WIDTH, OLED_HEIGHT, i2c)


def detectState(flag):
    state = "CLEAR"
    if flag == True:
        state = "OBS"
    return state

def doFlag(r):
    flag  = False
    if r<15:
        flag = True
    return flag

def doFlagZero(r):
    flag  = False
    if r == 0:
        flag = True
    #print("r",r,"flag",flag)
    return flag

def doSteer(front,right,left):
    steer = "fwd"
    if front:
        if right and left:
            steer = "stop"
            return steer
        if right and not left:
            steer = "left"
        else:
            steer = "right"
    return steer

### Loop ##########################
dl = drawList(oled, "DETECT")
dl.clear()
dl.scale(1,25)
dl.drawTitle()
done = False
try:
    print("----------------")
    print("Program started.")
    print()
    print("**** Wiring and Setup ****")
    print("* User Button defined at {}.".format(USER_BUTTON_PIN))
    print("* Left Detect Sensor defined at {}.".format(DETECT_LEFT_PIN))
    print("* Right Detect Sensor defined at {}.".format(DETECT_RIGHT_PIN))
    print("* Ultrasonic Sensor TRIG={}.".format(sonic.trigger))
    print("* Ultrasonic Sensor ECHO={}.".format(sonic.echo))
    print("* I2C defined at {}.".format(i2c))
    print("* OLED(I2C) defined as WIDE={} pixels x HIGH={} pixels.".format(OLED_WIDTH,OLED_HEIGHT))
    print("****************")
    print("\n")
    print("Press User Button or Press Control-c in Shell to exit.")
    done = False
    cnt = 0
    while not done:
        user_btn = user.value()
        if user_btn == 0:
            for cnt in range(1,70):
                #r = random.randint(1,dl.hi)
                #r2 = random.randint(0,1)
                #r3 = random.randint(0,1)
                
                distance = sonic.distance_cm()
                print("Distance= {:3.1f} cm.".format(distance))
                
                left_state = detect_left.value()
                right_state = detect_right.value()
                
                dl.drawData("uSonic",distance,1)
                dl.drawText("FRONT",detectState(doFlag(distance)),2)
                dl.drawText("RIGHT",detectState(doFlagZero(right_state)),3)
                dl.drawText("LEFT",detectState(doFlagZero(left_state)),4)
                dl.drawText("STEER",doSteer(doFlag(distance),doFlagZero(right_state),doFlagZero(left_state)),5)
                dl.show()
                time.sleep(2)
            dl.clear()
        time.sleep(0.2)
except KeyboardInterrupt:
    done = True
    print('Interrupted by Control-c.')
finally:
    oled.poweroff()
    oled = None
    sonic = None
    print('Finished.')

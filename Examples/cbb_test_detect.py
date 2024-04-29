# cbb_test_detect.py
#
# Copyright (C) 2024 KW Services.
# MIT License
# MicroPython 1.20
#
from pyb import LED
from machine import Pin, I2C
import time

### PIN Definitions ###############
# Builtin LED on the BlackPill.
BUILTIN_LED_NUM = 1
# Pin PB10 is dedicated "wired" to the user button.
USER_BUTTON_PIN = 'PB10'
# IR Detect
DETECT_PIN = 'PA0'

### Setup #########################
led = LED(BUILTIN_LED_NUM)
led.off()
user = Pin(USER_BUTTON_PIN, Pin.IN, Pin.PULL_UP)
detect = Pin(DETECT_PIN, Pin.IN, Pin.PULL_UP)

### Loop ########################## 
done = False
try:
    print("----------------")
    print("Program started.")
    print("*********************************************")
    print(" Board must have battery power connected.")
    print("*********************************************")
    print()
    print("**** Wiring and Setup ****")
    print("* Builtin LED at {}.".format(led))
    print("* User Button defined at {}.".format(USER_BUTTON_PIN))
    print("* Detect Sensor defined at {}.".format(DETECT_PIN))
    print("****************")
    print("\n")
    print("Detect is active!!! Press Control-c in Shell to exit.")
    done = False
    cnt = 0
    while not done:
        for r in range(0,10):
            detect_state = detect.value()
            if detect_state == 0:
                led.on()
                cnt = cnt + 1
                break
        if detect_state == 0:
            print("Detected count:{}.".format(cnt))
        led.off()
        time.sleep(0.5)
except KeyboardInterrupt:
    done = True
    print('Interrupted by Control-c.')
finally:
    led.off()
    print('Finished.')
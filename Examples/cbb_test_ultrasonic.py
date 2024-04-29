# cbb_test_ultrasonic.py
#
# Copyright (C) 2024 KW Services.
# MIT License
# MicroPython 1.20
#
from pyb import LED
from machine import Pin, I2C
import time

##### flash drive ################
# driver file: hcsr04.py must be on flash drive of BlackPill
# ultraSonic device is HC-SR04 (or HC-SR05)
from hcsr04 import HCSR04

### PIN Definitions ##############

# Builtin LED on the BlackPill.
BUILTIN_LED_NUM = 1
# Pin PB10 is dedicated "wired" to the user button.
USER_BUTTON_PIN = 'PB10'

#Car Base Board expects HCSR05 device which works at 3.3 volt
# connect a 5-pin cable to device
#SONIC_TRIG_PIN = 'PB8'
#SONIC_ECHO_PIN = 'PB9'

#Inland device HCSR04 requires five (5) volt line
# Cannot use the Sonic port
# plug 3-pin cable to adjoining three pins and a separate GND cable
SONIC_TRIG_PIN = 'PB9'
SONIC_ECHO_PIN = 'PB8'

### Setup #########################

led = LED(BUILTIN_LED_NUM)
led.off()
user = Pin(USER_BUTTON_PIN, Pin.IN, Pin.PULL_UP)
sonic = HCSR04(trigger_pin=SONIC_TRIG_PIN, echo_pin=SONIC_ECHO_PIN,echo_timeout_us=1000000)
time.sleep(0.2)

### Loop ##########################
       
done = False
try:
    print("----------------")
    print("Program started.")
    print("**** Wiring and Setup ****")
    print("* Builtin LED at {}.".format(led))
    print("* User Button defined at {}.".format(USER_BUTTON_PIN))
    print("* ultrasonic device.")
    print("    TRIG at {}".format(sonic.trigger ))
    print("    ECHO at {}".format(sonic.echo ))
    print("****************")
    print("\n")
    print("Press User button to read ultrasonic or Control-c in Shell to exit.")
    done = False
    while not done:
        user_btn = user.value()
        if user_btn == 0:
            led.on()
            distance = sonic.distance_cm()       
            print("Distance= {:3.1f} cm.".format(distance))
        led.off()
        time.sleep(0.5)
except KeyboardInterrupt:
    done = True
    print('Interrupted by Control-c.')
finally:
    led.off()
    print('Finished.')	


# cbb_test_motor_a.py
#
# Copyright (C) 2024 KW Services.
# MIT License
# MicroPython 1.20
#
from pyb import Pin, Timer, UART

import time
import gc

### PIN Definitions ##############
USER_BUTTON_PIN = 'PB10'
BUILTIN_LED_PIN = 'PC13'

# Pin Definitions for Motor A (L298N Device).
MOTORB_EN_PIN = 'PA3'
MOTOR_IN3_PIN = 'PB4'
MOTOR_IN4_PIN = 'PB5'

TIMER_MOTORB = 2
TIMER_MOTORB_CHANNEL = 4

### Setup #########################
user = Pin(USER_BUTTON_PIN, Pin.IN, Pin.PULL_UP)

enb = Pin(MOTORB_EN_PIN, Pin.OUT)
in3 = Pin(MOTOR_IN3_PIN, Pin.OUT)
in4 = Pin(MOTOR_IN4_PIN, Pin.OUT)

# Setup PWM.
pwmbtimer = Timer(TIMER_MOTORB, freq=500)
pwmbchannel = pwmbtimer.channel(TIMER_MOTORB_CHANNEL, Timer.PWM, pin=enb)

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
    print("* User Button defined at {}.".format(USER_BUTTON_PIN))
    print("* Car Motor B")
    print("    Motor B Pins: [EnB is {}] In3 is {} In4 is {}."
      .format(MOTORB_EN_PIN,MOTOR_IN3_PIN,MOTOR_IN4_PIN))
    print("    EnB setup for PWM: {}.".format(pwmbchannel))
    print("****************")
    print("\n")
    print("Press User button to turn on Motor B or Control-c in Shell to exit.")
    done = False 
    while not done:
        user_btn = user.value()
        if user_btn == 0:
            user_btn = 1
            # Operate.
            print("Motor A forward for one second.")
            in3.on()
            in4.off()
            pwmbchannel.pulse_width_percent(100)
            time.sleep(1)
            pwmbchannel.pulse_width_percent(0)
            time.sleep(1)
            print("Motor A reverse for one second.")
            in3.off()
            in4.on()
            pwmbchannel.pulse_width_percent(100)
            time.sleep(1)
            pwmbchannel.pulse_width_percent(0)
            done = True
        time.sleep(.5)
except KeyboardInterrupt:
    done = True
    print('Interrupted by Control-c.')
finally:
    pwmbtimer.deinit()
    print("Program end.")
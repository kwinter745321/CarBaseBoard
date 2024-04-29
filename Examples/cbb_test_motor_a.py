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
MOTORA_EN_PIN = 'PA2'
MOTOR_IN1_PIN = 'PA15'
MOTOR_IN2_PIN = 'PB3'

TIMER_MOTORA = 2
TIMER_MOTORA_CHANNEL = 3

### Setup #########################
user = Pin(USER_BUTTON_PIN, Pin.IN, Pin.PULL_UP)

ena = Pin(MOTORA_EN_PIN, Pin.OUT)
in1 = Pin(MOTOR_IN1_PIN, Pin.OUT)
in2 = Pin(MOTOR_IN2_PIN, Pin.OUT)

# Setup PWM.
pwmatimer = Timer(TIMER_MOTORA, freq=500)
pwmachannel = pwmatimer.channel(TIMER_MOTORA_CHANNEL, Timer.PWM, pin=ena)

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
    print("* Car Motor A")
    print("    Motor A Pins: [EnA is {}] In1 is {} In2 is {}."
      .format(MOTORA_EN_PIN,MOTOR_IN1_PIN,MOTOR_IN2_PIN))
    print("    EnA setup for PWM: {}.".format(pwmachannel))
    print("****************")
    print("\n")
    print("Press User button to turn on Motor A or Control-c in Shell to exit.")
    done = False 
    while not done:
        user_btn = user.value()
        if user_btn == 0:
            user_btn = 1
            # Operate.
            print("Motor A forward for one second.")
            in1.on()
            in2.off()
            pwmachannel.pulse_width_percent(100)
            time.sleep(1)
            pwmachannel.pulse_width_percent(0)
            time.sleep(1)
            print("Motor A reverse for one second.")
            in1.off()
            in2.on()
            pwmachannel.pulse_width_percent(100)
            time.sleep(1)
            pwmachannel.pulse_width_percent(0)
            done = True
        time.sleep(.5)
except KeyboardInterrupt:
    done = True
    print('Interrupted by Control-c.')
finally:
    pwmatimer.deinit()
    print("Program end.")
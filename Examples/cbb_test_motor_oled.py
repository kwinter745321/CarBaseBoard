# cbb_test_motor_oled.py
#
# Copyright (C) 2024 KW Services.
# MIT License
# MicroPython 1.20
#
from pyb import Pin, Timer
from machine import I2C
import time
import math
import random
import array

##### flash drive ################
# driver file: ssd1306.py must be on flash drive of BlackPill
import ssd1306
# lib file: cbb_oled_lib.py must be on flash drive of BlackPill
from cbb_oled_lib import drawList

### PIN Definitions ###############
# Define the Pins for the 4-socket hearder label I2C1 Port.
SCL_PIN = 'PB6'
SDA_PIN = 'PB7'
# Initialization of the I2C1 device
i2c = I2C(scl=Pin(SCL_PIN), sda=Pin(SDA_PIN), freq=100000)
# Parameter setting of screen characteristics in Pixels
OLED_WIDTH = 128
OLED_HEIGHT = 64

oled = ssd1306.SSD1306_I2C(OLED_WIDTH, OLED_HEIGHT, i2c)
print("* I2C1 is {}.".format(i2c))
##################################################
USER_BUTTON_PIN = 'PB10'
BUILTIN_LED_PIN = 'PC13'

key = Pin(USER_BUTTON_PIN, Pin.IN, Pin.PULL_UP)
led = (BUILTIN_LED_PIN, Pin.OUT)
##################################################
user = Pin(USER_BUTTON_PIN, Pin.IN, Pin.PULL_UP)
# Pin Definitions for Motor A/B (L298N Device)
MOTORA_EN_PIN = 'PA2'
MOTOR_IN1_PIN = 'PA15'
MOTOR_IN2_PIN = 'PB3'

MOTORB_EN_PIN = 'PA3'
MOTOR_IN3_PIN = 'PB4'
MOTOR_IN4_PIN = 'PB5'

ena = Pin(MOTORA_EN_PIN, Pin.OUT)
in1 = Pin(MOTOR_IN1_PIN, Pin.OUT)
in2 = Pin(MOTOR_IN2_PIN, Pin.OUT)
enb = Pin(MOTORB_EN_PIN, Pin.OUT)
in3 = Pin(MOTOR_IN3_PIN, Pin.OUT)
in4 = Pin(MOTOR_IN4_PIN, Pin.OUT)

# Pin Definition for Motor A/B Speed Sensors
SENSORA_PIN = 'PB1'  
SENSORB_PIN = 'PB2'

# Global variables and Call Back Functions
countera = 0
counterb = 0
show_a = True
show_b = True
line = 1

pwmatimer = Timer(2, freq=500)
pwmbtimer = Timer(2, freq=500)
# PWM.
pwmachannel = pwmatimer.channel(3, Timer.PWM, pin=ena)
pwmbchannel = pwmbtimer.channel(4, Timer.PWM, pin=enb)
print("PWM Timer for Motor A:{} \n Channel:{}".format(pwmatimer,pwmachannel))
print("PWM Timer for Motor B:{} \n Channel:{}".format(pwmbtimer,pwmbchannel))

sensora = None
sensorb = None

#drawlist display for OLED
dl = None
#Interrupt callbacks for Speed Sensor
def counta(pin):
    global countera
    countera = countera + 1
    return

def countb(pin):
    global counterb
    counterb = counterb + 1
    return

######################################

# Setup Interrupt Call Back Functions
def SetupMotorsAndSpeedSensors(SENSORA_PIN,SENSORB_PIN):
    global sensora, sensorb
    # Infrared (IR) Slotted Optical Speed Sensor.
    sensora = Pin(SENSORA_PIN, Pin.IN)
    sensorb = Pin(SENSORB_PIN, Pin.IN)
    print("Speed1 is using {}.".format(SENSORA_PIN))
    print("Speed2 is using {}.".format(SENSORB_PIN))
    # Handle Interrupts.
    sensora.irq(trigger=Pin.IRQ_FALLING, handler=counta)
    sensorb.irq(trigger=Pin.IRQ_FALLING, handler=countb)
    return

def startMotors():
    #start it spinning
    pwmachannel.pulse_width_percent(100)
    pwmbchannel.pulse_width_percent(100)
    time.sleep(0.5)

def calcRPM(mspeed):
    global countera, counterb, dl, line
    countera = 0
    counterb = 0
    print("Operate Motor A and B @ {}% for five seconds.".format(mspeed))
    t1 = time.time()
    t2 = time.time()
    while (t2-t1) < 5:
        t2 = time.time()
        pwmachannel.pulse_width_percent(mspeed)
        pwmbchannel.pulse_width_percent(mspeed)
    pwmachannel.pulse_width_percent(0)
    pwmbchannel.pulse_width_percent(0)
    time.sleep(0.5)
    print("A:{} cnts B:{} cnts".format(countera,counterb))
    # scale up to 12*5 sec then divide by 20 cnts/rotation
    elapsed = t2 - t1
    # rotations=counter divided by 20 cnts/rotation
    # gear speed = (rotations divided by elapsed time) * 60 sec/min 
    gearspeeda = (countera*3)/elapsed
    gearspeedb = (counterb*3)/elapsed
    # RPM is gear divided by 2 Pi
    rpma = gearspeeda /(2 * math.pi)
    rpmb = gearspeedb /(2 * math.pi)
    #rpma = (countera*3)/5
    #rpmb = (counterb*3)/5
    print("A:{} RPM B:{} RPM".format(rpma,rpmb))
    # OLED display
    text = "{:3.0f} {:5.1f} {:5.1f}".format(mspeed,rpma, rpmb)
    dl.drawText(text,"",line)
    dl.show()
    #time.sleep(1)
            
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
    print("* Car Motor B")
    print("    Motor B Pins: [EnB is {}] In3 is {} In4 is {}."
      .format(MOTORB_EN_PIN,MOTOR_IN3_PIN,MOTOR_IN4_PIN))
    print("    EnB setup for PWM: {}.".format(pwmbchannel))
    print("****************")
    SetupMotorsAndSpeedSensors(SENSORA_PIN,SENSORB_PIN)
    print("\n")
    print("Press User button to begin or Control-c in Shell to exit.")
    user_btn = user.value()
    while user_btn == 1:
        user_btn = user.value()
        time.sleep(0.2)
    print("Turn on power to Motors.")
    # Init display on OLED
    steps = 100
    show_a = True
    show_b = False
    print("*******************************************")
    print("**** Enable Motors forward for ten seconds to calculate RPM")
    print("**** Show counter for Motor A: {} and Motor B: {}".format(show_a,show_b))
    print("*******************************************")
    prompt = "Press User Button to start. Ctrl-C to exit."
    print(prompt)
    while not done:
        user_btn = user.value()
        #print("Key:",key_btn)
        if user_btn == 0:
            # Operate.
            line = 1
            dl = drawList(oled, "RPM")
            dl.clear()
            dl.scale(100,50)
            dl.drawTitle()
            dl.drawHeader("Sp%   A     B")
            dl.show()            
            print("start motor A and B going forward")
            in1.on()
            in2.off()
            in3.on()
            in4.off()
            startMotors()
            for speed in range(100,40,-10):
                calcRPM(speed)
                line = line + 1
            print(prompt)
        time.sleep(0.2)
except KeyboardInterrupt:
    done = True
    dl.clear()
    print('Interrupted by Control-c.')
    # Make sure counters are done spinning
    time.sleep(1)
finally:
    pwmatimer.deinit()
    pwmbtimer.deinit()
    time.sleep(5)
    print("Program end.")


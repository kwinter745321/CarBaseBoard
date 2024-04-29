# test_RPM_SpeedSensor.py
#
# Copyright (C) 2024 KW Services.
# MIT License
# MicroPython 1.20 
#
from pyb import Pin, Timer, UART
import time
import math
##################################################
USER_BUTTON_PIN = 'PB10'
BUILTIN_LED_PIN = 'PC13'

key = Pin(USER_BUTTON_PIN, Pin.IN, Pin.PULL_UP)
led = (BUILTIN_LED_PIN, Pin.OUT)
##################################################

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

pwmatimer = Timer(2, freq=500)
pwmbtimer = Timer(2, freq=500)
# PWM.
pwmachannel = pwmatimer.channel(3, Timer.PWM, pin=ena)
pwmbchannel = pwmbtimer.channel(4, Timer.PWM, pin=enb)
print("PWM Timer for Motor A:{} \n Channel:{}".format(pwmatimer,pwmachannel))
print("PWM Timer for Motor B:{} \n Channel:{}".format(pwmbtimer,pwmbchannel))

sensora = None
sensorb = None

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

def calcRPM(mspeed):
    global countera, counterb
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
    # scale up to 12*5 sec then divide by 20 cnts/revolution
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
    #time.sleep(1)
            
print("Program Begin.")
done = False
steps = 20
show_a = True
show_b = False
print("*******************************************")
print("**** Enable Motors forward for ten seconds to calculate RPM")
print("**** Show counter for Motor A: {} and Motor B: {}".format(show_a,show_b))
print("*******************************************")
print("Press User Button to start. Ctrl-C to exit.")
try: 
    while not done:
        key_btn = key.value()
        #print("Key:",key_btn)
        if key_btn == 0:
            key_btn = 1
            # Operate.
            SetupMotorsAndSpeedSensors(SENSORA_PIN,SENSORB_PIN)
            print("start motor A and B going forward")
            in1.on()
            in2.off()
            in3.on()
            in4.off()
            for speed in range(100,40,-10):
                calcRPM(speed)
            print("Done.")
            done = True
except KeyboardInterrupt:
    done = True
    print('Interrupted by Control-c.')
    # Make sure counters are done spinning
    time.sleep(1)
finally:
    pwmatimer.deinit()
    pwmbtimer.deinit()
    print("Program end.")
